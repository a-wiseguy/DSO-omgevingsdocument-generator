from copy import deepcopy
from typing import Any, Dict, List, Optional
from bs4 import BeautifulSoup

from lxml import etree
from io import StringIO

from app.tekst import divisie_to_xml, html_to_divisie
from app.tekst.tekst import Divisie, Lichaam


class PolicyObject:
    def __init__(self, data: dict):
        self._data: dict = data

    # @todo: maybe we should just give the html as a property to this api
    # instead of the Description, Explanation fields etc etc
    def html(self, context: dict = {}) -> str:
        match self._data['Object_Type']:
            case "visie_algemeen":
                return f"""
                    {self._html_title(context)}
                    {self._data['Description']}
                    """
            case "ambitie":
                return f"""
                    {self._html_title(context)}
                    {self._data['Description']}
                    """
            case "beleidskeuze":
                return f"""
                    {self._html_title(context)}
                    <h2>Omschrijving</h2>
                    {self._data['Description']}
                    <h2>Redenering</h2>
                    {self._data['Cause']}
                    """
        raise NotImplementedError()

    def _html_title(self, context: dict = {}) -> str:
        heading_number = context.get("heading_number")
        heading_number_attr = f' data-nummer="{heading_number}"' if heading_number is not None else ""
        return f"<h1{heading_number_attr}>{self._data['Title']}</h1>"

    def get(self, key: str, default: Any = None):
        return self._data.get(key, default)

    # def xml(self, context: dict = {}) -> str:
    #     html: str = self.html(context)
    #     divisie: Divisie = html_to_divisie(html)
    #     xml: str = divisie_to_xml(divisie)
    #     return xml


class PolicyObjects:
    def __init__(self, data: dict):
        self._data: Dict[str, List[PolicyObject]] = {
            object_type: [PolicyObject(o) for o in objects]
            for object_type, objects in data.items()
        }

    def get_all(self, object_type: str) -> List[PolicyObject]:
        return deepcopy(self._data.get(object_type, []))

    def get_optional(self, object_type: str, object_id: int) -> Optional[PolicyObject]:
        for o in self.get_all(object_type):
            if o.get("Object_ID", 0) == object_id:
                return o
        return None

    def get(self, object_type: str, object_id: int) -> PolicyObject:
        o: Optional[PolicyObject] = self.get_optional(object_type, object_id)
        if o is None:
            raise RuntimeError(f"Can not find object {object_type}-{object_id}")
        return o


def visie_algemeen_as_html(o: dict, heading_number: Optional[int] = None) -> str:
    heading_number_attr: str = ""
    if heading_number is not None:
        heading_number_attr = f' data-nummer="{heading_number}"'
    html = f"""<h1{heading_number_attr}>{o['Title']}</h1>{o['Description']}"""
    return html


def is_html_valid(html_content) -> bool:
    try:
        parser = etree.HTMLParser(recover=False)
        etree.parse(StringIO(html_content), parser)
        return True
    except etree.XMLSyntaxError:
        return False


def html_to_xml_lichaam(html: str) -> str:
    if not is_html_valid(html):
        raise RuntimeError("Invalid html")

    input_soup = BeautifulSoup(html, "html.parser")
    lichaam = Lichaam()
    lichaam.consume_children(input_soup.children)

    output_soup = BeautifulSoup(features='xml')
    output = lichaam.as_xml(output_soup)
    output_xml = str(output)
    return output_xml
