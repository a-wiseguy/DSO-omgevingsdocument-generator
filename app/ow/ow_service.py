from typing import List, Optional
from uuid import UUID
from jinja2.exceptions import TemplateNotFound

from app.gio.models import Werkingsgebied
from app.models import AKN
from .models import OWGebied, OWGebiedenGroep, OWDivisieTekst, OWTekstDeel, Annotation
from utils.helpers import (
    load_template_and_write_file,
    load_werkingsgebieden,
)


class OWServiceError(Exception):
    def __init__(self, message: str = "Exception building/creating OW files."):
        super().__init__(message)


class OWService:
    OW_REGEX = r"nl\.imow-(gm|pv|ws|mn|mnre)[0-9]{1,6}\.(regeltekst|gebied|...)"

    def __init__(self, id_levering: UUID, akn: AKN):
        self.id_levering = id_levering
        self.akn = akn

    def create_ow_file(self, ow_data, ow_template, output_path: str):
        try:
            load_template_and_write_file(
                template_name=ow_template,
                output_file=output_path,
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
            "objectTypen": ["Divisie", "Divisietekst", "Tekstdeel"],
            "gebiedengroepen": [],
            "gebieden": [],
        }
        # Create new OW Locations
        for werkingsgebied in werkingsgebieden:
            ow_locations = [
                OWGebied(geo_uuid=loc.UUID) for loc in werkingsgebied.Locaties
            ]
            ow_group = OWGebiedenGroep(
                geo_uuid=werkingsgebied.UUID, locations=ow_locations
            )
            xml_data["gebieden"].extend(ow_locations)
            xml_data["gebiedengroepen"].append(ow_group)

        return xml_data

    def build_ow_divisies(self, annotations):
        xml_data = {
            "leveringsId": self.id_levering,
            "objectTypen": ["Divisietekst", "Tekstdeel"],
            "annotaties": [],
        }

        for annotation in annotations:
            ow_div = OWDivisieTekst(wid=annotation["wid"])
            ow_text = OWTekstDeel(
                divisie=ow_div.OW_ID, locations=annotation["locations"]
            )
            new_annotation = Annotation(divisie=ow_div, tekstdeel=ow_text)
            xml_data["annotaties"].append(new_annotation)

        return xml_data

    def create_all_ow_files(self):
        divisie_output_path = "output/owDivisie.xml"
        divisie_template = "templates/ow/owDivisie.xml"
        location_output_path = "output/owLocaties.xml"
        location_template = "templates/ow/owLocaties.xml"
        manifest_output_path = "output/manifest-ow.xml"
        manifest_template = "templates/ow/manifest-ow.xml"

        # owLocation
        werkingsgebieden = load_werkingsgebieden()
        locaties_data = self.build_ow_locaties(werkingsgebieden)
        self.create_ow_file(
            ow_data=locaties_data,
            ow_template=location_template,
            output_path=location_output_path,
        )

        # owDivisie
        annotations = [
            {
                "wid": "pv28_2093__content_1",
                "locations": [
                    "nl.imow-pv28.gebiedengroep.002000000000000000000036",
                    "nl.imow-pv28.gebiedengroep.002000000000000000000038",
                ],
            },
            {
                "wid": "pv28_2093__content_2",
                "locations": [
                    "nl.imow-pv28.ambtsgebied.002000000000000000009928",
                ],
            },
        ]

        divisie_data = self.build_ow_divisies(annotations)
        self.create_ow_file(
            ow_data=divisie_data,
            ow_template=divisie_template,
            output_path=divisie_output_path,
        )

        # Manifest
        self.create_ow_file(
            ow_data={
                "act_akn": self.akn.as_FRBR().work,
                "doel_id": self.akn.as_doel(),
            },
            ow_template=manifest_template,
            output_path=manifest_output_path,
        )
