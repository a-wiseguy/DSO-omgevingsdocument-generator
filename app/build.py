from uuid import uuid4
from typing import Optional, List, Dict
from jinja2.exceptions import TemplateNotFound
from app.assets.create_image import create_image
from app.assets.assets_service import AssetsService
from app.assets.enrich_illustratie import middleware_enrich_illustratie

from app.ewid.ewid_service import EWIDService
from app.exceptions import PublicationServiceError
from app.models import (
    AKN,
    Besluit,
    BestuursDocument,
    ProcedureVerloop,
    Regeling,
    DocumentType,
    PublicationSettings,
    PublicatieOpdracht,
    Bestand,
)
from app.policy_objects import PolicyObjects
from app.publication_document.models import (
    OmgevingsProgramma,
    OmgevingsVisie,
    PublicationDocument,
)
from utils.waardelijsten import OnderwerpType, RechtsgebiedType, ProcedureType
from utils.helpers import load_template_and_write_file


class PublicationService:
    DEFAULT_OUTPUT_PATH = "output/"

    def __init__(
        self,
        settings: PublicationSettings,
        akn: Optional[AKN],
        input_data: dict,
        assets_service: AssetsService,
    ):
        self._settings: PublicationSettings = settings
        self._input_data = input_data
        self._document: PublicationDocument
        self._files: List[Bestand] = []
        self._assets_service: AssetsService = assets_service

        if akn:
            self._akn = akn
        else:
            self._akn = AKN(
                province_id=settings.provincie_id,
                previous_act=settings.previous_akn_act,
                previous_bill=settings.previous_akn_bill,
            )

    def setup_publication_document(self, input_data=None) -> PublicationDocument:
        if input_data is None:
            input_data = self._input_data

        bestuurs_document = BestuursDocument(
            eindverantwoordelijke=self._settings.provincie_id,
            maker=self._settings.provincie_ref,
            soort_bestuursorgaan="/tooi/def/thes/kern/c_411b4e4a",
            onderwerp=OnderwerpType.ruimtelijke_ordening.value,
            rechtsgebied=RechtsgebiedType.Omgevingsrecht.value,
        )

        besluit = Besluit(
            **input_data["besluit"],
            frbr=self._akn.as_FRBR(akn_type="bill"),
            bestuurs_document=bestuurs_document,
            soort_procedure=ProcedureType.Definitief_besluit,
        )

        regeling = Regeling(
            **input_data["regeling"],
            frbr=self._akn.as_FRBR(akn_type="act"),
            bestuurs_document=bestuurs_document,
        )

        procedure = ProcedureVerloop(**input_data["procedure"])

        if self._settings.document_type is DocumentType.VISIE:
            initial_document = OmgevingsVisie(
                bill=besluit, act=regeling, procedure=procedure
            )
        elif self._settings.document_type is DocumentType.PROGRAMMA:
            initial_document = OmgevingsProgramma(
                bill=besluit, act=regeling, procedure=procedure
            )
        else:
            raise PublicationServiceError(
                message="Expected DocumentType Visie or Programma"
            )

        self._document = initial_document
        return initial_document

    def create_publication_document(
        self,
        objects: PolicyObjects,
        document: PublicationDocument,
        output_path=DEFAULT_OUTPUT_PATH,
    ):
        lichaam = document.generate_regeling_vrijetekst_lichaam(objects)
        lichaam = middleware_enrich_illustratie(self._assets_service, lichaam)
        wid_prefix = f"{self._settings.provincie_id}_{self._settings.previous_akn_bill}"
        ewid_service = EWIDService(xml=lichaam, wid_prefix=wid_prefix)
        lichaam = ewid_service.fill_ewid_in_str()
        try:
            write_path = output_path + self._akn.as_filename()
            load_template_and_write_file(
                template_name="templates/base/AanleveringBesluit.xml",
                output_file=write_path,
                omgevingsdocument_template=document.template,
                akn=self._akn.as_dict(),
                regeling=document.act,
                besluit=document.bill,
                procedure=document.procedure,
                vrijetekst_lichaam=lichaam,
                pretty_print=True,
            )
            print(f"Created {self._akn} - path: {write_path}")
            return write_path
        except TemplateNotFound as e:
            raise PublicationServiceError(
                message=f"child template not while writing xml: {e}"
            )
        except Exception as e:
            raise PublicationServiceError(message=e)

    def create_lvbb_manifest(self, output_path=DEFAULT_OUTPUT_PATH):
        try:
            write_path = output_path + "manifest.xml"
            load_template_and_write_file(
                template_name="templates/lvbb/manifest.xml",
                output_file=write_path,
                bestanden=self._files,
                akn=str(self._akn),
                pretty_print=True,
            )
            print(f"Created manifest.xml in: {output_path}")
            return write_path
        except TemplateNotFound as e:
            raise PublicationServiceError(
                message=f"Manifest file Template missing: {e}"
            )
        except Exception as e:
            raise PublicationServiceError(message=e)

    def create_opdracht(
        self, opdracht: PublicatieOpdracht = None, output_path=DEFAULT_OUTPUT_PATH
    ):
        if not opdracht:
            opdracht = PublicatieOpdracht(
                id_levering=uuid4(),
                publicatie=self._akn.as_filename(),
                datum_bekendmaking=self._settings.public_release_date,
            )
        try:
            write_path = output_path + "opdracht.xml"
            load_template_and_write_file(
                template_name="templates/lvbb/opdracht.xml",
                output_file=write_path,
                publicatieopdracht=opdracht,
                pretty_print=True,
            )
            print(f"Created opdracht.xml in: {write_path}")
            return opdracht
        except TemplateNotFound as e:
            raise PublicationServiceError(
                message=f"Opdracht file Template missing: {e}"
            )
        except Exception as e:
            raise PublicationServiceError(message=e)

    def add_geo_files(self, gio_files: List[Bestand], gml_refs: List[str]):
        # merge in the geo service files/references
        if self._document is None:
            raise PublicationServiceError(
                "PublicationDocument not initialized. cannot add geo files."
            )
        self._files = self._files + gio_files
        self._document.bill.informatieobject_refs = (
            self._document.bill.informatieobject_refs + gml_refs
        )

    def create_images(self):
        for asset in self._assets_service.all():
            path: str = f"output/{asset.get_filename()}"
            create_image(asset, path)
            self._files.append(
                Bestand(
                    bestandsnaam=asset.get_filename(),
                    content_type=asset.Meta.Formaat,
                )
            )

    def build_publication_files(self, objects: PolicyObjects):
        if self._document is None:
            if self._input_data is None:
                raise PublicationServiceError(
                    "Missing expected input data from publication document."
                )
            self.setup_publication_document(self._input_data)

        self.create_images()
        publication_file_output = self.create_publication_document(
            objects=objects, document=self._document
        )
        self.create_lvbb_manifest()
        opdracht = self.create_opdracht()
        return opdracht
