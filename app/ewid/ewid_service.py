import re
from bs4 import Tag


class EIDGenerationError(Exception):
    def __init__(self, element, message="Error in generating eID"):
        self.element = element
        self.message = message
        super().__init__(self.message)


class EWIDService:
    FIXED_ELEMENT_REF = {
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

    def __init__(self, soup: Tag = None, wid_prefix: str = "pv28_0000"):
        self.eId_counter = {}
        self.soup = soup
        self.wid_prefix = wid_prefix

    def fill_ewid_in_bs4(self):
        self._process_ewid_element(self.soup, wid_prefix=self.wid_prefix)
        return self.soup

    def _process_ewid_element(self, element, wid_prefix: str, parent_eid=None, num_counter=None):
        """
        recursivly follow the child elements path and create a hierarchical eid
        using the tags prefix. ensures wids are unique.
        https://koop.gitlab.io/STOP/standaard/1.3.0/eid_wid.html
        """
        eid = self._generate_eid(element, parent_eid)
        if eid is not None:
            element['eId'] = eid
            wid = f"{wid_prefix}__{eid}"
            element['wid'] = wid

        if eid and num_counter is not None:
            if 'num' not in element.attrs:
                num_counter.setdefault(eid, 0)
                num_counter[eid] += 1
                element['eId'] = f"{eid}_o_{num_counter[eid]}"

        for child in element.children:
            if hasattr(child, 'name') and child.name:
                if eid:
                    child_num_counter = num_counter if num_counter is not None else {}
                    self._process_ewid_element(child, wid_prefix, eid, child_num_counter)
                else:
                    self._process_ewid_element(child, wid_prefix, parent_eid, num_counter)

    def _generate_eid(self, element, parent_eid=None):
        """
        Create a unique eid based on element name and hierarchy.
        """
        try:
            ref = self.FIXED_ELEMENT_REF.get(element.name, None)
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
