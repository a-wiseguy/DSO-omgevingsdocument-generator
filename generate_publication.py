import uuid
from jinja2 import Environment, FileSystemLoader

from utils.helpers import load_template_and_write_file, load_json_data, get_file_entries
from utils.waardelijsten import (
    Provincie,
    ProcedureStappenDefinitief,
    RegelingType,
    WorkType,
    PublicatieType,
)

env = Environment(loader=FileSystemLoader("."))

# Content type mapping for building file manifests
content_type_map = {
    "xml": "application/xml",
    "gml": "application/gml+xml",
    "jpg": "image/jpeg",
    "pdf": "application/pdf",
}

# TODO: generate real AKN
PUBLICATIE_AKN = "akn_nl_bill_pv28-2-2093"
PZH_ID = "pv28"
PZH_REF = Provincie.Zuid_Holland.value

# Input data for templates
regeling = {
    "FRBRWork": f"/akn/nl/act/{PZH_ID}/2023/2_41",
    "FRBRExpression": f"/akn/nl/act/{PZH_ID}/2023/2_41/nld@2093",
    "soortWork": WorkType.Regeling.value,
    "versienummer": "v1",
    "soortRegeling": RegelingType.Omgevingsvisie.value,
    "eindverantwoordelijke": PZH_REF,
    "maker": PZH_REF,
    "soortBestuursorgaan": "/tooi/def/thes/kern/c_411b4e4a",
    "officieleTitel": "dossier naam Hello World Programma",
    "citeertitel": "citeertitel programma hello World",
    "isOfficieel": "true",
    "onderwerp": "/tooi/def/concept/c_9af4b880",
    "rechtsgebied": "/tooi/def/concept/c_638d8062",
}

besluit_versie = {
    "FRBRWork": "/akn/nl/bill/new_work/2023/2_3000",
    "FRBRExpression": "/akn/nl/bill/new_work/2023/2_3000/nld@2023-10-01;3000",
    "soortWork": WorkType.Besluit.value,
    "eindverantwoordelijke": PZH_REF,
    "maker": PZH_REF,
    "soortBestuursorgaan": "/tooi/def/thes/kern/c_new",
    "officieleTitel": "New Title for the Program",
    "onderwerp": "/tooi/def/concept/c_new1",
    "rechtsgebied": "/tooi/def/concept/c_new2",
    "soortProcedure": PublicatieType.Bekendmaking.value,
    "informatieobjectRef": [  # Gio refs?
        "/join/id/regdata/new_province/2023/new_pdf",
        "/join/id/regdata/new_province/2023/new_gio1",
        "/join/id/regdata/new_province/2023/new_gio2",
    ],
}

besluit_compact = {
    "RegelingOpschrift": "regeling dossier naam Hello World Programma",
    "Aanhef": "dossier naam Hello World Programma",
    "WijzigArtikel_Label": "Artikel",
    "WijzigArtikel_Nummer": "I",
    "WijzigArtikel_Wat": "zoals is aangegeven in Bijlage A bij Artikel I",
    "Artikelen": [
        {
            "eId": "art_II",
            "wId": "pv28_1__art_II",
            "Label": "Artikel",
            "Nummer": "II",
            "Inhoud": None,
        },
        {
            "eId": "art_III",
            "wId": "pv28_1__art_III",
            "Label": "Artikel",
            "Nummer": "III",
            "Inhoud": "Dit besluit treedt in werking op de dag waarop dit bekend wordt gemaakt.",
        },
    ],
    "Sluiting": "Gegeven te 's-Gravenhage, 27 september 2023",
    "Ondertekening": "-",
}


publicatie_opdracht = {
    "idLevering": uuid.uuid4(),  # uuid of publication or per LVBB "inlevering"
    "idBevoegdGezag": "00000001002306608000",
    "idAanleveraar": "00000003011411800000",
    "publicatie": f"{PUBLICATIE_AKN}.xml",
    "datumBekendmaking": "2023-09-30",
}

# https://gitlab.com/koop/lvbb/bronhouderkoppelvlak/-/blob/1.2.0/waardelijsten/procedurestap_definitief.xml?ref_type=tags
procedure_metadata = {
    "bekendOp": publicatie_opdracht["datumBekendmaking"],
    "stappen": [
        {"soortStap": ProcedureStappenDefinitief.Vaststelling.value, "voltooidOp": "2023-09-27"},
        {"soortStap": ProcedureStappenDefinitief.Ondertekening.value, "voltooidOp": "2023-09-27"},
    ],
}

# Write LVBB PublicatieOpdracht
load_template_and_write_file(
    "templates/lvbb/opdracht.xml",
    "output/opdracht.xml",
    publicatieopdracht=publicatie_opdracht,
)

# Write LVBB Manifest
file_entries = get_file_entries("input/attachments", content_type_map)
load_template_and_write_file(
    "templates/lvbb/manifest.xml", "output/manifest.xml", file_entries=file_entries
)

# Load policy objects
json_data = load_json_data("input/policy-objects/mock-data.json")
ambities = json_data["ambities"]
beleidskeuzes = json_data["beleidskeuzes"]

# Write full regeling
load_template_and_write_file(
    "templates/visie.xml",
    f"output/{PUBLICATIE_AKN}.xml",
    regeling=regeling,
    besluitversie=besluit_versie,
    besluitcompact=besluit_compact,
    procedure=procedure_metadata,
    ambities=ambities,
    beleidskeuzes=beleidskeuzes,
)
