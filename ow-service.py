import re
import glob
from typing import List, Optional
from uuid import uuid4, UUID
from pydantic import BaseModel, Field

from enum import Enum
from app.gio.models import Werkingsgebied

from utils.helpers import load_json_data, load_template_and_write_file

OW_REGEX = r"nl\.imow-(gm|pv|ws|mn|mnre)[0-9]{1,6}\.(regeltekst|gebied|gebiedengroep|lijn|lijnengroep|punt|puntengroep|activiteit|gebiedsaanwijzing|omgevingswaarde|omgevingsnorm|pons|kaart|tekstdeel|hoofdlijn|divisie|kaartlaag|juridischeregel|activiteitlocatieaanduiding|normwaarde|regelingsgebied|ambtsgebied|divisietekst)\.[A-Za-z0-9]{1,32}"


class IMOWTYPES(Enum):
    REGELTEKST = "regeltekst"
    GEBIED = "gebied"
    GEBIEDENGROEP = "gebiedengroep"
    LIJN = "lijn"
    LIJNENGROEP = "lijnengroep"
    PUNT = "punt"
    PUNTENGROEP = "puntengroep"
    ACTIVITEIT = "activiteit"
    GEBIEDSAANWIJZING = "gebiedsaanwijzing"
    OMGEVINGSWAARDE = "omgevingswaarde"
    OMGEVINGSNORM = "omgevingsnorm"
    PONS = "pons"
    KAART = "kaart"
    TEKSTDEEL = "tekstdeel"
    HOOFDLIJN = "hoofdlijn"
    DIVISIE = "divisie"
    KAARTLAAG = "kaartlaag"
    JURIDISCHEREGEL = "juridischeregel"
    ACTIVITEITLOCATIEAANDUIDING = "activiteitlocatieaanduiding"
    NORMWAARDE = "normwaarde"
    REGELINGSGEBIED = "regelingsgebied"
    AMBTSGEBIED = "ambtsgebied"
    DIVISIETEKST = "divisietekst"


def generate_ow_id(ow_type: IMOWTYPES, organisation_id: str = "pv28"):
    prefix = f"nl.imow-{organisation_id}"
    unique_code = uuid4()
    generated_id = f"{prefix}.{ow_type.value}.{unique_code.hex}"

    imow_pattern = re.compile(OW_REGEX)
    if not imow_pattern.match(generated_id):
        raise Exception("generated IMOW ID does not match official regex")

    return generated_id


class OWObject(BaseModel):
    OW_ID: str


class OWLocation(OWObject):
    geo_uuid: UUID
    noemer: Optional[str] = None


class OWGebied(OWLocation):
    OW_ID: str = Field(default_factory=lambda: generate_ow_id(IMOWTYPES.GEBIED))


class OWGebiedenGroep(OWLocation):
    OW_ID: str = Field(default_factory=lambda: generate_ow_id(IMOWTYPES.GEBIEDENGROEP))
    locations: List[OWGebied] = []


class OWDivisieTekst(OWObject):
    OW_ID: str = Field(default_factory=lambda: generate_ow_id(IMOWTYPES.DIVISIETEKST))
    wid: str


class OWTekstDeel(OWObject):
    OW_ID: str = Field(default_factory=lambda: generate_ow_id(IMOWTYPES.TEKSTDEEL))
    divisie: str  # is divisie(tekst) OW_ID
    locations: List[str]  # OWlocation OW_ID list


class Annotation(BaseModel):
    divisie: OWDivisieTekst
    tekstdeel: OWTekstDeel


def load_werkingsgebieden() -> List[Werkingsgebied]:
    return [
        Werkingsgebied(**load_json_data(wg_json))
        for wg_json in glob.glob("./input/werkingsgebieden/*.json")
    ]


def build_ow_locaties():
    ow_locaties_xml_data = {
        "leveringsId": "00000000-0000-0000-0000-000000000000",
        "objectTypen": ["Divisie", "Divisietekst", "Tekstdeel"],
        "gebiedengroepen": [],
        "gebieden": [],
    }

    werkingsgebieden = load_werkingsgebieden()
    # Create new OW Locations
    for werkingsgebied in werkingsgebieden:
        ow_locations = [OWGebied(geo_uuid=loc.UUID) for loc in werkingsgebied.Locaties]
        ow_group = OWGebiedenGroep(geo_uuid=werkingsgebied.UUID, locations=ow_locations)
        ow_locaties_xml_data["gebieden"].extend(ow_locations)
        ow_locaties_xml_data["gebiedengroepen"].append(ow_group)

    write_path = "output/owLocaties.xml"
    load_template_and_write_file(
        template_name="templates/ow/owLocaties.xml",
        output_file=write_path,
        locaties=ow_locaties_xml_data,
        pretty_print=True,
    )

    # TODO: Store in DB / Log
    print("Created Gebieden GEO_UUID -> OW_ID")
    for gebied in ow_locaties_xml_data["gebieden"]:
        print(f"{gebied.geo_uuid} -> {gebied.OW_ID}")

    print("Created Groepen GEO_UUID -> OW_ID")
    for group in ow_locaties_xml_data["gebiedengroepen"]:
        print(f"{group.geo_uuid} -> {group.OW_ID}")


def build_ow_divisies():
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

    ow_divisies_xml_data = {
        "leveringsId": "00000000-0000-0000-0000-000000000000",
        "objectTypen": ["Divisietekst", "Tekstdeel"],
        "annotaties": [],
    }

    for annotation in annotations:
        ow_div = OWDivisieTekst(wid=annotation["wid"])
        ow_text = OWTekstDeel(divisie=ow_div.OW_ID, locations=annotation["locations"])
        new_annotation = Annotation(divisie=ow_div, tekstdeel=ow_text)
        ow_divisies_xml_data["annotaties"].append(new_annotation)

    write_path = "output/owDivisie.xml"
    load_template_and_write_file(
        template_name="templates/ow/owDivisie.xml",
        output_file=write_path,
        divisies=ow_divisies_xml_data,
        pretty_print=True,
    )


if __name__ == "__main__":
    build_ow_locaties()
    build_ow_divisies()
