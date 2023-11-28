import re
import xml.etree.ElementTree as ET
from enum import Enum
from bs4 import Tag


class FIXED_ELEMENT_REF(Enum):
    Aanhef = "formula_1"
    AlgemeneToelichting = "genrecital"
    ArtikelgewijzeToelichting = "artrecital"
    Inhoudsopgave = "toc"
    Lichaam = "body"
    Motivering = "acc"
    RegelingOpschrift = "longTitle"
    Sluiting = "formula_2 or formula_2_inst"
    Toelichting = "recital"


class ELEMENT_REF(Enum):
    Afdeling = "subchp"
    Artikel = "art"
    Begrip = "item"
    Begrippenlijst = "list"
    Bijlage = "cmp"
    Boek = "book"
    Citaat = "cit"
    Deel = "part"
    Divisie = "div"
    Divisietekst = "content"
    ExtIoRef = "ref"
    Figuur = "img"
    Formule = "math"
    Hoofdstuk = "chp"
    InleidendeTekst = "intro"
    IntIoRef = "ref"
    InwerkingtredingArtikel = "art"
    Kadertekst = "recital"
    Li = "item"
    Lid = "para"
    Lijst = "list"
    Paragraaf = "subsec"
    Rectificatietekst = "content"
    Subparagraaf = "subsec"
    Subsubparagraaf = "subsec"
    table = "table"
    Titel = "title"
    WijzigArtikel = "art"
    WijzigBijlage = "cmp"


class EIDGenerationError(Exception):
    def __init__(self, element, message="Error in generating eID"):
        self.element = element
        self.message = message
        super().__init__(self.message)


class EWIDService:
    fixed_element_ref = {e.name: e.value for e in FIXED_ELEMENT_REF}
    element_ref = {e.name: e.value for e in ELEMENT_REF}

    def __init__(self, xml, wid_prefix: str = "pv28_0000"):
        self.eId_counter = {}
        self.xml = self._parse_xml_to_etree(xml)
        self.wid_prefix = wid_prefix

    def _parse_xml_to_etree(self, xml_string):
        try:
            tree = ET.ElementTree(ET.fromstring(xml_string))
            root = tree.getroot()
            return root
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            raise EIDGenerationError(xml_string, str(e))

    def fill_ewid_in_bs4(self):
        self._process_ewid_element(self.xml, wid_prefix=self.wid_prefix)
        return self.xml

    def fill_ewid_in_str(self):
        self._process_ewid_element(self.xml, wid_prefix=self.wid_prefix)
        output: str = ET.tostring(self.xml, encoding="utf-8").decode("utf-8")
        return output

    def _process_ewid_element(self, element, wid_prefix: str, parent_eid=None, num_counter=None):
        """
        Recursively follow the child elements path and create a hierarchical eid
        using the tags prefix. Ensures wids are unique.
        https://koop.gitlab.io/STOP/standaard/1.3.0/eid_wid.html
        """
        eid = self._generate_eid(element, parent_eid)
        if eid is not None:
            element.set("eId", eid)
            wid = f"{wid_prefix}__{eid}"
            element.set("wId", wid)

        if eid and num_counter is not None:
            if element.get("num") is None:
                num_counter.setdefault(eid, 0)
                num_counter[eid] += 1
                element.set("eId", f"{eid}_o_{num_counter[eid]}")

        # Determine the parent eid for child elements
        child_parent_eid = eid if not self.fixed_element_ref.get(element.tag) else parent_eid

        for child in list(element):
            if isinstance(child.tag, str):
                child_num_counter = num_counter if num_counter is not None else {}
                self._process_ewid_element(
                    child, wid_prefix, child_parent_eid, child_num_counter
                )

    def _generate_eid(self, element, parent_eid=None):
        """
        Create a unique eid based on element name and hierarchy.
        """
        try:
            # skip if element is a fixed ref
            ref = self.fixed_element_ref.get(element.tag, None)
            if ref:
                return ref

            ref = self.element_ref.get(element.tag, None)
            if ref is None:
                return None

            num = ""
            if element.get("num"):  # if element has a num attribute, use it
                num = "_" + self._get_sanitized_number(element.get("num"))
            elif not parent_eid:  # for top-level elements without a num
                num = "_o_1"

            if parent_eid:
                eid = f"{parent_eid}__{ref}{num}"
            else:
                eid = f"{ref}{num}"

            eid = self._ensure_unique_eid(eid)
            return eid
        except Exception as e:
            raise EIDGenerationError(element, str(e))

    def _ensure_unique_eid(self, eid):
        """
        Make eID unique if needed
        """
        if eid not in self.eId_counter:
            self.eId_counter[eid] = 1
            return eid
        else:
            self.eId_counter[eid] += 1
            return f"{eid}_inst{self.eId_counter[eid]}"

    def _get_sanitized_number(self, text):
        """
        Generate the number part of the eId
        """
        text = text.replace(" ", "")
        text = re.sub(r"[^0-9a-zA-Z\.-]", ".", text)
        text = re.sub(r"\.+$", "", text)  # remove trailing dot
        return text