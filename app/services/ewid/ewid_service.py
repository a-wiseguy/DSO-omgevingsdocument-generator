import re
import xml.etree.ElementTree as ET

from app.builder.state_manager.state_manager import StateManager
from app.services.ewid import ELEMENT_REF, FIXED_ELEMENT_REF, EIDGenerationError


class EWIDService:
    """
    The EWIDService class is responsible for generating EWID for policy objects.
    """

    fixed_element_ref = {e.name: e.value for e in FIXED_ELEMENT_REF}
    element_ref = {e.name: e.value for e in ELEMENT_REF}

    def __init__(self, state_manager: StateManager, xml_string, wid_prefix="pv28_0000"):
        self._state_manager: StateManager = state_manager

        self.eId_counter = {}
        self.wid_prefix = wid_prefix
        self.xml_tree = self._parse_xml_to_etree(xml_string)

    def fill_ewid(self):
        """
        Recursively parses XML tree and adds eId and wId attributes to elements.

        Returns:
            str: The XML tree as a string.
        """
        self._process_ewid_element(self.xml_tree, wid_prefix=self.wid_prefix)
        output: str = ET.tostring(self.xml_tree, encoding="utf-8").decode("utf-8")
        return output

    def _parse_xml_to_etree(self, xml_string):
        """
        Parses an XML string and returns the root element as an ElementTree object.

        Args:
            xml_string (str): The XML string to parse.

        Returns:
            Element: The root element of the parsed XML.

        Raises:
            EIDGenerationError: If there is an error parsing the XML.
        """
        try:
            tree = ET.ElementTree(ET.fromstring(xml_string))
            root = tree.getroot()
            return root
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            raise EIDGenerationError(xml_string, str(e))

    def _process_ewid_element(self, element, wid_prefix: str, parent_eid=None, num_counter=None):
        """
        Recursively follow the child elements path and create a hierarchical eid
        using the tags prefix. Ensures wids are unique.

        Args:
            element (Element): The XML element to process.
            wid_prefix (str): The prefix to use for generating the wid.
            parent_eid (str, optional): The parent eid. Defaults to None.
            num_counter (dict, optional): A counter for tracking the number of child elements. Defaults to None.

        Returns:
            None
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

        # Remember the EWID for location annotated policy objects
        if "data-hint-object-code" in element.attrib or "data-hint-location" in element.attrib:
            object_code = element.get("data-hint-object-code", None)
            gebied_uuid = element.get("data-hint-gebied-uuid", None)
            # Store pairing in state
            self._state_manager.object_tekst_lookup[object_code] = {
                "wid": wid,
                "tag": element.tag,
                "gebied_uuid": gebied_uuid,
            }

        # Determine the parent eid for child elements
        child_parent_eid = eid if not self.fixed_element_ref.get(element.tag) else parent_eid

        for child in list(element):
            if isinstance(child.tag, str):
                child_num_counter = num_counter if num_counter is not None else {}
                self._process_ewid_element(child, wid_prefix, child_parent_eid, child_num_counter)

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

            # generate num part of eId
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
            # increment counter for doubles
            self.eId_counter[eid] += 1
            return f"{eid}_inst{self.eId_counter[eid]}"

    def _get_sanitized_number(self, text):
        """
        Generate the number part of the eId
        """
        text = text.replace(" ", "")
        # remove all non-alphanumeric characters except dot and dash
        text = re.sub(r"[^0-9a-zA-Z\.-]", ".", text)
        # remove leading and trailing dots
        text = re.sub(r"\.+$", "", text)
        return text
