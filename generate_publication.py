import json
import os
from jinja2 import Environment, FileSystemLoader


# Helpers
def load_template_and_write_file(template_name, output_file, **context):
    template = env.get_template(template_name)
    output = template.render(**context)
    with open(output_file, "w") as f:
        f.write(output)


def get_file_entries(folder_path, content_type_map):
    file_entries = []
    for filename in os.listdir(folder_path):
        extension = filename.split(".")[-1]
        content_type = content_type_map.get(extension)
        file_entries.append({"filename": filename, "contentType": content_type})
    return file_entries


def load_json_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


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

# Input data for templates
regeling = {
    "FRBRWork": "/akn/nl/act/pv28/2023/2_41",
    "FRBRExpression": "/akn/nl/act/pv28/2023/2_41/nld@2093",
    "soortWork": "/join/id/stop/work_019",
    "versienummer": "v1",
    "soortRegeling": "/join/id/stop/regelingtype_010",
    "eindverantwoordelijke": "/tooi/id/provincie/pv28",
    "maker": "/tooi/id/provincie/pv28",
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
    "soortWork": "/join/id/stop/new_work_004",
    "eindverantwoordelijke": "/tooi/id/provincie/new_province",
    "maker": "/tooi/id/provincie/new_province",
    "soortBestuursorgaan": "/tooi/def/thes/kern/c_new",
    "officieleTitel": "New Title for the Program",
    "onderwerp": "/tooi/def/concept/c_new1",
    "rechtsgebied": "/tooi/def/concept/c_new2",
    "soortProcedure": "/join/id/stop/new_proceduretype",
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
    "idLevering": "382fafad-8a0c-4d19-9b2e-12f1980ca310", # uuid of publication or per LVBB "inlevering"
    "idBevoegdGezag": "00000001002306608000",
    "idAanleveraar": "00000003011411800000",
    "publicatie": f"{PUBLICATIE_AKN}.xml",
    "datumBekendmaking": "2023-09-30",
}

procedure_metadata = {
    "bekendOp": publicatie_opdracht["datumBekendmaking"],
    "stappen": [
        {"soortStap": "/join/id/stop/procedure/stap_002", "voltooidOp": "2023-09-27"},
        {"soortStap": "/join/id/stop/procedure/stap_003", "voltooidOp": "2023-09-27"},
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
