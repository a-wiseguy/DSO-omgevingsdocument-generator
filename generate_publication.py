from typing import List
import uuid
import glob
from jinja2 import Environment, FileSystemLoader
from app.gio.gio_service import GioService
from app.gio.models import Werkingsgebied
from app.models import FRBR, Besluit, Bestand, BestuursDocument, ProcedureStap, ProcedureVerloop, Regeling

from utils.helpers import load_template_and_write_file, load_json_data, get_file_entries
from utils.geo import parse_gml_metadata
from utils.waardelijsten import (
    ProcedureType,
    Provincie,
    ProcedureStappenDefinitief,
    RegelingType,
    WorkType,
    PublicatieType,
    RechtsgebiedType,
    OnderwerpType,
)

env = Environment(loader=FileSystemLoader("."))

# Content type mapping for building file manifests
content_type_map = {
    "xml": "application/xml",
    "gml": "application/gml+xml",
    "jpg": "image/jpeg",
    "pdf": "application/pdf",
}

DSO_VERSIONING = {
    "STOP": "1.3.0",
    "TPOD": "2.0.2",
    "LVBB": "1.2.0",
}

# TODO: generate real AKN
PUBLICATIE_AKN = "akn_nl_bill_pv28-2-2093"
PZH_ID = "pv28"
PZH_REF = Provincie.Zuid_Holland.value
DATUM_BEKENDMAKING = "2023-09-30"



# Input data for templates
# regeling = {
#     "FRBRWork": f"/akn/nl/act/{PZH_ID}/2023/2_41",
#     "FRBRExpression": f"/akn/nl/act/{PZH_ID}/2023/2_41/nld@2093",
#     "soortWork": WorkType.Regeling.value,
#     "versienummer": "v1",
#     "soortRegeling": RegelingType.Omgevingsvisie.value,
#     "eindverantwoordelijke": PZH_REF,
#     "maker": PZH_REF,
#     "soortBestuursorgaan": "/tooi/def/thes/kern/c_411b4e4a",
#     "officieleTitel": "dossier naam Hello World Programma",
#     "citeertitel": "citeertitel programma hello World",
#     "isOfficieel": "true",
#     "onderwerp": OnderwerpType.ruimtelijke_ordening.value,
#     "rechtsgebied": RechtsgebiedType.omgevingsrecht.value,
# }


# @todo: calculate
bestuurs_document: BestuursDocument = BestuursDocument(
    eindverantwoordelijke=PZH_REF,
    maker=PZH_REF,
    soort_bestuursorgaan="/tooi/def/thes/kern/c_411b4e4a",
    onderwerp=OnderwerpType.ruimtelijke_ordening.value,
    rechtsgebied=RechtsgebiedType.omgevingsrecht.value,
)


besluit_frbr = FRBR(
    work=f"/akn/nl/bill/{PZH_ID}/2023/2_3000",
    expression=f"/akn/nl/bill/{PZH_ID}/2023/2_3000/nld@2023-10-01;2093",
)
besluit: Besluit = Besluit(
    frbr=besluit_frbr,
    bestuurs_document=bestuurs_document,
    officiele_titel="Opschrift besluit - Dossier naam Hello World Programma",
    soort_procedure=ProcedureType.Definitief_besluit,
)

regeling_frbr = FRBR(
    work=f"/akn/nl/act/{PZH_ID}/2023/2_41",
    expression=f"/akn/nl/act/{PZH_ID}/2023/2_41/nld@2093",
)
regeling: Regeling = Regeling(
    frbr=regeling_frbr,
    bestuurs_document=bestuurs_document,
    versienummer="v1",
    officiele_titel="Dossier naam Hello World Programma",
    citeertitel="citeertitel programma hello World",
    is_officieel="true",
)



# besluit_versie = {
#     "FRBRWork": "/akn/nl/bill/new_work/2023/2_3000",
#     "FRBRExpression": "/akn/nl/bill/new_work/2023/2_3000/nld@2023-10-01;3000",
#     "soortWork": WorkType.Besluit.value,
#     "eindverantwoordelijke": PZH_REF,
#     "maker": PZH_REF,
#     "soortBestuursorgaan": "/tooi/def/thes/kern/c_new",
#     "officieleTitel": "dossier naam Hello World Programma",
#     "onderwerp": OnderwerpType.ruimtelijke_ordening.value,
#     "rechtsgebied": RechtsgebiedType.omgevingsrecht.value,
#     "soortProcedure": PublicatieType.Bekendmaking.value,
#     "informatieobjectRef": [  # Gio refs?
#         "/join/id/regdata/new_province/2023/new_pdf",
#         "/join/id/regdata/new_province/2023/new_gio1",
#         "/join/id/regdata/new_province/2023/new_gio2",
#     ],
# }

besluit_compact = {
    "RegelingOpschrift": "regeling dossier naam Hello World Programma",
    "Aanhef": "dossier naam Hello World Programma",
    "WijzigArtikel": {
        "Label": "Artikel",
        "Nummer": "I",
        "Wat": "zoals is aangegeven in Bijlage A bij Artikel I",
    },
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
    "WijzigingBijlage": {
        "Label": "Bijlage",
        "Nummer": "A",
        "Opschrift": "Bijlage bij Artikel I",
    },
    "Sluiting": "Gegeven te 's-Gravenhage, 27 september 2023",
    "Ondertekening": "-",
}


publicatie_opdracht = {
    "idLevering": uuid.uuid4(),  # uuid of publication or per LVBB "inlevering"
    "idBevoegdGezag": "00000001002306608000",
    "idAanleveraar": "00000003011411800000",
    "publicatie": f"{PUBLICATIE_AKN}.xml",
    "datumBekendmaking": DATUM_BEKENDMAKING,
}

# https://gitlab.com/koop/lvbb/bronhouderkoppelvlak/-/blob/1.2.0/waardelijsten/procedurestap_definitief.xml?ref_type=tags
procedure: ProcedureVerloop = ProcedureVerloop(
    bekend_op=DATUM_BEKENDMAKING,
    stappend = [
        ProcedureStap(
            soort_stap=ProcedureStappenDefinitief.Vaststelling.value,
            voltooid_op="2023-09-27",
        ),
        ProcedureStap(
            soort_stap=ProcedureStappenDefinitief.Ondertekening.value,
            voltooid_op="2023-09-27",
        ),
    ]
)


# Write LVBB PublicatieOpdracht
load_template_and_write_file(
    "templates/lvbb/opdracht.xml",
    "output/opdracht.xml",
    publicatieopdracht=publicatie_opdracht,
)

# Generate GIO files
bestanden: List[Bestand] = []
gio_service = GioService(regeling)

werkingsgebieden_jsons = glob.glob("./input/werkingsgebieden/*.json")
for werkingsgebieden_json in werkingsgebieden_jsons:
    data = load_json_data(werkingsgebieden_json)
    werkingsgebied = Werkingsgebied(**data)
    gio_service.add_werkingsgebied(werkingsgebied)

gio_files: List[Bestand] = gio_service.generate_files()
bestanden = bestanden + gio_files

gml_refs: List[str] = gio_service.get_refs()
besluit.informatieobject_refs = besluit.informatieobject_refs + gml_refs


# TODO: IO files


# Write LVBB Manifest
load_template_and_write_file(
    "templates/lvbb/manifest.xml",
    "output/manifest.xml",
    bestanden=bestanden,
    akn=PUBLICATIE_AKN,
    pretty_print=True,
)

# Load policy objects
json_data = load_json_data("input/policy-objects/mock-data.json")
ambities = json_data["ambities"]
beleidskeuzes = json_data["beleidskeuzes"]

# Write full regeling
load_template_and_write_file(
    "templates/AanleveringBesluit.xml",
    f"output/{PUBLICATIE_AKN}.xml",
    regeling=regeling,
    besluit=besluit,

    besluitcompact=besluit_compact,
    procedure=procedure,
    ambities=ambities,
    beleidskeuzes=beleidskeuzes,

    pretty_print=True,
)
