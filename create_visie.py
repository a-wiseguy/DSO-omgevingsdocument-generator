import json
import os
from jinja2 import Environment, FileSystemLoader

# Ambitie data endpoint list
# https://api-obzh.azurewebsites.net/ambities/valid?limit=20&offset=0&sort_column=Title&sort_order=ASC
# Ambitie data detail call
# https://api-obzh.azurewebsites.net/ambities/version/*UUID*

env = Environment(loader=FileSystemLoader("."))

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
    "informatieobjectRef": [
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

procedure_metadata = {
    "bekendOp": "2023-09-30",
    "stappen": [
        {"soortStap": "/join/id/stop/procedure/stap_002", "voltooidOp": "2023-09-27"},
        {"soortStap": "/join/id/stop/procedure/stap_003", "voltooidOp": "2023-09-27"},
    ],
}

publicatie_opdracht = {
    "idLevering": "382fafad-8a0c-4d19-9b2e-12f1980ca310",
    "idBevoegdGezag": "00000001002306608000",
    "idAanleveraar": "00000003011411800000",
    "publicatie": "akn_nl_bill_pv28-2-2093.xml",
    "datumBekendmaking": "2023-09-30",
}


# LVBB PublicatieOpdracht
opdracht_template = env.get_template("templates/lvbb/opdracht.xml")
opdracht_xml = opdracht_template.render(publicatieopdracht=publicatie_opdracht)
with open("output/opdracht.xml", "w") as f:
    f.write(opdracht_xml)

# LVBB Manifest
content_type_map = {
    "xml": "application/xml",
    "gml": "application/gml+xml",
    "jpg": "image/jpeg",
    "pdf": "application/pdf",
}

file_entries = []

for filename in os.listdir("input/attachments"):
    extension = filename.split(".")[-1]
    contentType = content_type_map.get(extension, "application/octet-stream")
    file_entries.append({"filename": filename, "contentType": contentType})

template = env.get_template("templates/lvbb/manifest.xml")
output = template.render(file_entries=file_entries)

with open("output/manifest.xml", "w") as f:
    f.write(output)


###
# Export full regeling
###

ambities = []
beleidskeuzes = []

# API policy objects to populate the template
with open("input/policy-objects/mock-data.json", "r") as f:
    json_data = json.load(f)
    ambities = json_data["ambities"]
    beleidskeuzes = json_data["beleidskeuzes"]

template = env.get_template("templates/visie.xml")
xml_output = template.render(
    regeling=regeling,
    besluitversie=besluit_versie,
    besluitcompact=besluit_compact,
    procedure=procedure_metadata,
    ambities=ambities,
    beleidskeuzes=beleidskeuzes,
)

# Export regeling
with open("output/visie.xml", "w") as f:
    f.write(xml_output)
