from io import StringIO
from typing import Optional

from bs4 import BeautifulSoup
from lxml import etree

from app.tekst.middleware import middleware_enrich_table
from app.tekst.tekst import Lichaam


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

    html = middleware_enrich_table(html)
    input_soup = BeautifulSoup(html, "html.parser")
    lichaam = Lichaam()
    lichaam.consume_children(input_soup.children)

    output_soup = BeautifulSoup(features="xml")
    output = lichaam.as_xml(output_soup)
    output_xml = str(output)
    return output_xml
