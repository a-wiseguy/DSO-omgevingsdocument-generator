import xml.etree.ElementTree as ET

# TODO: Trying to serialize policy objects properly with matching ID/Attributes,
# then insert back into template


def generate_ambitie(amb, div_position=1):
    eId = f"div_{div_position}__content_{div_position}"
    wId = f"pv28_1067__div_{div_position}__content_{div_position}"

    root = ET.Element("Divisietekst", {"eId": eId, "wId": wId})

    kop = ET.SubElement(root, "Kop")
    opschrift = ET.SubElement(kop, "Opschrift")
    opschrift.text = f"Ambitie ID {amb['Object_ID']}"
    inhoud = ET.SubElement(root, "Inhoud")
    al_title = ET.SubElement(inhoud, "Al")
    al_title.text = f"Ambitie {amb['Title']}"
    al_desc = ET.SubElement(inhoud, "Al")
    al_desc.text = amb["Description"]

    return ET.tostring(root).decode("utf-8")
