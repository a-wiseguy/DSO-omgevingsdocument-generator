from typing import List, Optional
from uuid import UUID

from jinja2.exceptions import TemplateNotFound

from app.ewid import PolicyObjectReference
from app.gio.models import Werkingsgebied
from app.models import AKN
from utils.helpers import load_template_and_write_file, load_werkingsgebieden

from .models import Annotation, OWDivisieTekst, OWGebied, OWGebiedenGroep, OWTekstDeel


class OWServiceError(Exception):
    def __init__(self, message: str = "Exception building/creating OW files."):
        super().__init__(message)


class OWService:
    OW_REGEX = r"nl\.imow-(gm|pv|ws|mn|mnre)[0-9]{1,6}\.(regeltekst|gebied|...)"
    DEFAULT_OUTPUT_DIR = "output/"
    DEFAULT_TEMPLATE_DIR = "templates/ow/"

    def __init__(self, id_levering: UUID, akn: AKN):
        self.id_levering = id_levering
        self.akn = akn

    def create_ow_file(self, ow_data, ow_template, output_path: str):
        try:
            load_template_and_write_file(
                template_name=f"{self.DEFAULT_TEMPLATE_DIR}{ow_template}",
                output_file=f"{self.DEFAULT_OUTPUT_DIR}{output_path}",
                data=ow_data,
                pretty_print=True,
            )
            print(f"Created file: {output_path}")
            return output_path
        except TemplateNotFound as e:
            raise OWServiceError(message=f"OW file Template missing: {e}")
        except Exception as e:
            raise OWServiceError(message=str(e))

    def build_ow_locaties(self, werkingsgebieden: List[Werkingsgebied]):
        xml_data = {
            "leveringsId": self.id_levering,
            "objectTypen": ["Ambtsgebied"],
            "gebiedengroepen": [],
            "gebieden": [],
        }
        # Create new OW Locations
        for werkingsgebied in werkingsgebieden:
            ow_locations = [OWGebied(geo_uuid=loc.UUID, noemer=loc.Title) for loc in werkingsgebied.Locaties]
            ow_group = OWGebiedenGroep(
                geo_uuid=werkingsgebied.UUID,
                noemer=werkingsgebied.Title,
                locations=ow_locations,
            )
            xml_data["gebieden"].extend(ow_locations)
            xml_data["gebiedengroepen"].append(ow_group)

        # extend object types if needed
        if len(xml_data["gebieden"]) > 0:
            xml_data["objectTypen"].append("Gebied")
        if len(xml_data["gebiedengroepen"]) > 0:
            xml_data["objectTypen"].append("Gebiedengroep")

        return xml_data

    def build_ow_divisies(self, annotations: List[PolicyObjectReference]):
        xml_data = {
            "leveringsId": self.id_levering,
            "objectTypen": ["Divisietekst", "Tekstdeel"],  # TODO: make dynamic
            "annotaties": [],
        }

        for annotation in annotations:
            if not annotation.location:
                continue

            ow_div = OWDivisieTekst(wid=annotation.wid)
            ow_text = OWTekstDeel(divisie=ow_div.OW_ID, locations=[annotation.ow_location_id])
            new_annotation = Annotation(divisie=ow_div, tekstdeel=ow_text)
            xml_data["annotaties"].append(new_annotation)

        return xml_data

    def create_all_ow_files(self, annotations: List[PolicyObjectReference]):
        # owLocation
        werkingsgebieden = load_werkingsgebieden()
        locaties_data = self.build_ow_locaties(werkingsgebieden)
        self.create_ow_file(
            ow_data=locaties_data,
            ow_template="owLocaties.xml",
            output_path="owLocaties.xml",
        )

        ow_gebied_mapping = {gebied.geo_uuid: gebied.OW_ID for gebied in locaties_data["gebieden"]}
        ow_gebied_mapping.update(
            {gebiedengroep.geo_uuid: gebiedengroep.OW_ID for gebiedengroep in locaties_data["gebiedengroepen"]}
        )

        for annotation in annotations:
            if not annotation.location:
                continue

            # Find the matching OWGebied and update ow_location_id
            matching_ow_gebied = ow_gebied_mapping.get(UUID(annotation.location))
            if matching_ow_gebied:
                annotation.ow_location_id = matching_ow_gebied

        # owDivisie
        divisie_data = self.build_ow_divisies(annotations)
        self.create_ow_file(
            ow_data=divisie_data,
            ow_template="owDivisie.xml",
            output_path="owDivisie.xml",
        )

        # owRegelingsgebied
        self.create_ow_file(
            ow_data={"leveringsId": self.id_levering},
            ow_template="owRegelingsgebied.xml",
            output_path="owRegelingsgebied.xml",
        )

        # Manifest
        self.create_ow_file(
            ow_data={
                "act_akn": self.akn.as_FRBR().work,
                "doel_id": self.akn.as_doel(),
            },
            ow_template="manifest-ow.xml",
            output_path="manifest-ow.xml",
        )
