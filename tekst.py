from abc import ABC, abstractmethod
from calendar import c
from typing import Dict, List, Optional
from lxml import etree
from bs4 import BeautifulSoup, CData, Comment, Declaration, Doctype, NavigableString, ProcessingInstruction, Tag

from data import html_content


html_content = """
<h1>Title</h1>
<p>Line 1</p>
<p>Text with <em>important</em> parts</p>
"""

expected_output = """
<Divisie>
    <Kop>
        <Opschrift>Title</Opschrift>
    </Kop>
    <Inhoud>
        <Al>Line 1</Al>
        <Al>Text with <i>important</i> parts</Al>
    </Inhoud>
</Divisie>
"""


class Element(ABC):
    def apply_begin(self, soup: BeautifulSoup) -> Optional[Tag]:
        return None


class Ignored(Element):
    pass


class P(Element):
    def apply_begin(self, soup: BeautifulSoup) -> Optional[Tag]:
        return soup.new_tag("Al")



class InputACC:
    def __init__(self):
        self._acc: List[Element] = []
    
    def add(self, element: Element):
        self._acc.append(element)
    
    def pop(self) -> Element:
        element = self._acc.pop()
        return element


class Output:
    def __init__(self):
        self._soup: BeautifulSoup = BeautifulSoup("", "html.parser")
        self._node: Tag = self._soup

    def begin_element(self, element: Element):
        
    
    def end_element(self, element: Element):
        pass

    def add_tag(self, name: str):
        node: Tag = self._soup.new_tag(name)
        self._node.append(node)
        self._node = node


class Parser:
    def __init__(self, html_content: str):
        self._html_content: str = html_content

        self._input_soup = BeautifulSoup(self._html_content, "html.parser")
        self._input_acc: InputACC = InputACC()

        self._output: Output = Output()

        self._allowed_tags_map: Dict[str, Element] = {
            "p": P,
            # "h1": H,
        }
    
    def parse(self):
        self._output.add_tag("Divisie")
        self._walk(self._input_soup)

    def _walk(self, node):
        for element in node.children:
            if isinstance(element, Tag):
                print(f"Tag: {element.name}")
                self._handle_tag(element)
            elif isinstance(element, NavigableString):
                print(f"String: {element}")
            elif isinstance(element, Comment):
                raise NotImplementedError("Comment", element)
            elif isinstance(element, Doctype):
                raise NotImplementedError("Doctype", element)
            elif isinstance(element, CData):
                raise NotImplementedError("CData", element)
            elif isinstance(element, ProcessingInstruction):
                raise NotImplementedError("ProcessingInstruction", element)
            elif isinstance(element, Declaration):
                raise NotImplementedError("Declaration", element)
            else:
                raise Exception("Unknown type", element)

    def _handle_tag(self, tag: Tag):
        element: Element = self._allowed_tags_map.get(tag.name, Ignored)
        if isinstance(element, Ignored):
            print(f"Tag '{tag.name}' is not allowed")

        self._output.begin_element(element)
        # if tag.is_empty_element:


        
        




parser = Parser(html_content)
parser.parse()
