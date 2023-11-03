from typing import Optional, List
from enum import Enum

from pydantic import BaseModel
from jinja2.exceptions import TemplateNotFound

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
from utils.waardelijsten import OnderwerpType, RechtsgebiedType, ProcedureType
from utils.helpers import load_template_and_write_file, load_json_data


class PublicationDocument(BaseModel):
    template: Optional[str]
    input_data: Optional[str]
    bill: Optional[Besluit]
    act: Optional[Regeling]
    procedure: Optional[ProcedureVerloop]


class OmgevingsVisie(PublicationDocument):
    template: Optional[str] = "templates/omgevingsvisie/child_of_RegelingVrijetekst.xml"
    input_data: Optional[str] = "input/publication/omgevingsvisie.json"
    # ambities: Optional[List[str]] = None # TODO


class OmgevingsProgramma(PublicationDocument):
    template: Optional[str] = "templates/omgevingsprogramma/child_of_RegelingVrijetekst.xml"
    input_data: Optional[str] = "input/publication/omgevingsprogramma.json"
    # maatregelen: Optional[List[str]] = None # TODO


class LVBBPublication(BaseModel):
    akn: Optional[AKN]
    opdracht: Optional[PublicatieOpdracht]
    document: Optional[PublicationDocument]


class PublicationService:
    DEFAULT_OUTPUT_PATH = "output/"

    def __init__(self, settings: PublicationSettings, akn: Optional[AKN], input_file: str):
        self._settings: PublicationSettings = settings
        self._input_file = input_file
        self._document: PublicationDocument
        self._files: List[Bestand] = []

        if akn:
            self._akn = akn
        else:
            self._akn = AKN(
                province_id=settings.provincie_id,
                previous_act=settings.previous_akn_act,
                previous_bill=settings.previous_akn_bill,
            )

    def setup_publication_document(self, input_data_file=None) -> PublicationDocument:
        if input_data_file is None:
            input_data_file = self._input_file

        loaded_from_file = load_json_data(input_data_file)

        bestuurs_document = BestuursDocument(
            eindverantwoordelijke=self._settings.provincie_id,
            maker=self._settings.provincie_ref,
            soort_bestuursorgaan="/tooi/def/thes/kern/c_411b4e4a",
            onderwerp=OnderwerpType.ruimtelijke_ordening.value,
            rechtsgebied=RechtsgebiedType.Omgevingsrecht.value,
        )

        besluit = Besluit(
            **loaded_from_file["besluit"],
            frbr=self._akn.as_FRBR(akn_type="bill"),
            bestuurs_document=bestuurs_document,
            soort_procedure=ProcedureType.Definitief_besluit,
        )

        regeling = Regeling(
            **loaded_from_file["regeling"],
            frbr=self._akn.as_FRBR(akn_type="act"),
            bestuurs_document=bestuurs_document,
        )

        procedure = ProcedureVerloop(**loaded_from_file["procedure"])

        if self._settings.document_type is DocumentType.VISIE:
            initial_document = OmgevingsVisie(bill=besluit, act=regeling, procedure=procedure)
        elif self._settings.document_type is DocumentType.PROGRAMMA:
            initial_document = OmgevingsProgramma(bill=besluit, act=regeling, procedure=procedure)
        else:
            raise PublicationServiceError(message="Expected DocumentType Visie or Programma")

        self._document = initial_document
        return initial_document

    def create_publication_document(
        self, document: PublicationDocument, output_path=DEFAULT_OUTPUT_PATH
    ):
        # TODO build policy objects based on type
        # json_data = load_json_data("input/policy-objects/mock-data.json")
        # ambities = json_data["ambities"]
        # beleidskeuzes = json_data["beleidskeuzes"]
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
                pretty_print=True,
            )
            print(f"Created {self._akn} - path: {output_path}")
        except TemplateNotFound as e:
            raise PublicationServiceError(message=f"child template not while writing xml: {e}")
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
        except TemplateNotFound as e:
            raise PublicationServiceError(message=f"Manifest file Template missing: {e}")
        except Exception as e:
            raise PublicationServiceError(message=e)

    def create_opdracht(self, output_path=DEFAULT_OUTPUT_PATH):
        publicatieopdracht = PublicatieOpdracht(
            publicatie=self._akn.as_filename(), datum_bekendmaking=self._settings.publicatie_datum
        )
        try:
            write_path = output_path + "opdracht.xml"
            load_template_and_write_file(
                template_name="templates/lvbb/opdracht.xml",
                output_file=write_path,
                publicatieopdracht=publicatieopdracht,
                pretty_print=True,
            )
            print(f"Created opdracht.xml in: {output_path}")
        except TemplateNotFound as e:
            raise PublicationServiceError(message=f"Opdracht file Template missing: {e}")
        except Exception as e:
            raise PublicationServiceError(message=e)

    def add_geo_files(self, gio_files: List[Bestand], gml_refs: List[str]):
        # merge in the geo service files/references
        if self._document is None:
            raise PublicationServiceError("PublicationDocument not initialized. cannot add geo files.")
        self._files = self._files + gio_files
        self._document.bill.informatieobject_refs = (
            self._document.bill.informatieobject_refs + gml_refs
        )

    def build_publication_files(self):
        if self._document is None:
            if self._input_file is None:
                raise PublicationServiceError("Missing expected input data from publication document.")
            self.setup_publication_document(self._input_file)

        self.create_publication_document(document=self._document)
        self.create_lvbb_manifest()
        self.create_opdracht()