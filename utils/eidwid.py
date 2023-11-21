import xml.etree.ElementTree as ET
import re


element_ref = {
    "Afdeling": "subchp",
    "Artikel": "art",
    "Begrip": "item",
    "Begrippenlijst": "list",
    "Bijlage": "cmp",
    "Boek": "book",
    "Citaat": "cit",
    "Deel": "part",
    "Divisie": "div",
    "Divisietekst": "content",
    "ExtIoRef": "ref",
    "Figuur": "img",
    "Formule": "math",
    "Hoofdstuk": "chp",
    "InleidendeTekst": "intro",
    "IntIoRef": "ref",
    "InwerkingtredingArtikel": "art",
    "Kadertekst": "recital",
    "Li": "item",
    "Lid": "para",
    "Lijst": "list",
    "Paragraaf": "subsec",
    "Rectificatietekst": "content",
    "Subparagraaf": "subsec",
    "Subsubparagraaf": "subsec",
    "table": "table",
    "Titel": "title",
    "WijzigArtikel": "art",
    "WijzigBijlage": "cmp",
}


def get_sanitized_number(text):
    # generate the number part of the eId
    text = text.replace(" ", "")
    text = re.sub(r"[^0-9a-zA-Z\.-]", ".", text)
    text = re.sub(r"\.+$", "", text)  # Remove trailing dots
    return text


# Keep track of existing eIds to handle uniqueness
eId_counter = {}


def ensure_unique_eid(eid):
    # Make eID unique if needed
    global eId_counter
    if eid not in eId_counter:
        eId_counter[eid] = 1
        return eid
    else:
        eId_counter[eid] += 1
        return f"{eid}_inst{eId_counter[eid]}"


def generate_eid(element, parent_eid=None):
    ref = element_ref.get(element.tag, None)
    if ref is None:
        return None
    num = ""
    if element.get("num"):  # if element has a num attribute, use it
        num = "_" + get_sanitized_number(element.get("num"))
    elif not parent_eid:  # for top-level elements without a num
        num = "_o_1"

    if parent_eid:
        eid = f"{parent_eid}__{ref}{num}"
    else:
        eid = f"{ref}{num}"

    eid = ensure_unique_eid(eid)
    return eid


def process_element(
    element, parent_eid=None, num_counter=None, wid_prefix: str = "pv28_2069"
):
    eid = generate_eid(element, parent_eid)
    if eid is not None:
        element.set("eId", eid)
        # Generate wid using the custom prefix
        wid = f"{wid_prefix}__{eid}"
        element.set("wid", wid)

    # Handle non-explicitly numbered elements
    if eid and num_counter is not None:
        if not element.get("num"):
            num_counter.setdefault(eid, 0)
            num_counter[eid] += 1
            element.set("eId", f"{eid}_o_{num_counter[eid]}")

    # Recurse the child elements
    for child in list(element):
        if eid:
            # Initialize or pass down the num_counter for non-explicitly numbered children
            child_num_counter = num_counter if num_counter is not None else {}
            process_element(child, eid, child_num_counter)
        else:
            process_element(child, parent_eid, num_counter)


def generate_ew_ids(
    input_file="tmp/visie-vrijetekst.xml", output_file="tmp/output_vrijetekst.xml"
):
    tree = ET.parse(input_file)
    root = tree.getroot()
    process_element(root)
    tree.write(output_file, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    input_file = "tmp/visie-vrijetekst.xml"
    tree = ET.parse(input_file)
    root = tree.getroot()
    process_element(root)
    output_file = "tmp/output_wideid.xml"
    tree.write(output_file, encoding="UTF-8", xml_declaration=True)
