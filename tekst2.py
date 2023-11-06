from abc import ABC, abstractmethod
from calendar import c
from typing import Any, Dict, List, Optional, Union
from lxml import etree
from bs4 import BeautifulSoup, CData, Comment, Declaration, Doctype, NavigableString, ProcessingInstruction, Tag
from numpy import isin

from data import html_content


html_content = """
<h1>Title with a <em>bold</em> piece of text</h1>
<p>Line 1</p>
<p>Text with <em>important</em> parts</p>
"""

expected_output = """
<Divisie>
    <Kop>
        <Opschrift>Title</Opschrift>
    </Kop>
    <Divisietekst>
        <Inhoud>
            <Al>Line 1</Al>
            <Al>Text with <i>important</i> parts</Al>
        </Inhoud>
    </Divisietekst>
</Divisie>
"""




class I:
    def __init__(self):
        self.content: List[str] = [] # @todo should support other elements

    def consume_children(self, children: List[Any]):
        for element in children:
            if isinstance(element, Tag):
                print(f"Tag: {element.name}")
                self.consume_tag(element)
            elif isinstance(element, NavigableString):
                print(f"String: {element}")
                self.consume_string(element)
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

    def consume_tag(self, tag: Tag):
        if tag.name in ["i", "em"]:
            content = I()
            content.consume_children(tag.children)
            self.content.append(content)

    def consume_string(self, string: NavigableString):
        self.content.append(str(string))



class Kop:
    def __init__(self, tag: Optional[Tag] = None):
        self.opschrift: List[Union[I, str]] = []

    def consume_children(self, children: List[Any]):
        for element in children:
            if isinstance(element, Tag):
                print(f"Tag: {element.name}")
                self.consume_tag(element)
            elif isinstance(element, NavigableString):
                print(f"String: {element}")
                self.consume_string(element)
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

    def consume_tag(self, tag: Tag):
        if tag.name in ["i", "em"]:
            content = I()
            content.consume_children(tag.children)
            self.opschrift.append(content)

    def consume_string(self, string: NavigableString):
        self.opschrift.append(str(string))



class Al:
    def __init__(self):
        self.content: List[Union[str, I]] = []

    def consume_children(self, children: List[Any]):
        for element in children:
            if isinstance(element, Tag):
                print(f"Tag: {element.name}")
                self.consume_tag(element)
            elif isinstance(element, NavigableString):
                print(f"String: {element}")
                self.consume_string(element)
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

    def consume_tag(self, tag: Tag):
        if tag.name in ["i", "em"]:
            content = I()
            content.consume_children(tag.children)
            self.content.append(content)

    def consume_string(self, string: NavigableString):
        self.content.append(str(string))

class Inhoud:
    def __init__(self):
        # @todo add more see https://koop.gitlab.io/STOP/standaard/1.3.0/tekst_xsd_Element_tekst_Inhoud.html#Inhoud
        self.content_1: List[Al] = [] # mgBlocksMinimaal
        # self.content_2: List[Al] # mgBlocksVolledig

    def consume_tag(self, tag: Tag):
        # Headings will be send to the Kop
        if tag.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            raise RuntimeError("Tussenkop not implemented yet")
        elif tag.name == "p":
            alinea: Al = Al()
            alinea.consume_children(tag.children)
            self.content_1.append(alinea)
        else:
            raise RuntimeError(f"Unsupport tag {tag.name}")

    def consume_string(self, string: NavigableString):
        pass



class Divisietekst:
    def __init__(self):
        self.kop: Optional[Kop] = None
        self.inhoud: Optional[Inhoud] = None

    def consume_tag(self, tag: Tag):
        # Headings will be send to the Kop
        if tag.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            if self.kop is not None:
                # @todo: shall return new divisie-tekst and the title set
                raise RuntimeError("Double titles are not implemented yet")
            kop = Kop()
            kop.consume_children(tag.children)
            self.kop = kop
            return

        # Any other tags will just be send in a Inhoud
        inhoud: Inhoud = self._get_inhoud()
        inhoud.consume_tag(tag)
    
    def _get_inhoud(self) -> Inhoud:
        if self.inhoud == None:
            self.inhoud = Inhoud()
        
        return self.inhoud


class Divisie:
    def __init__(self):
        self.kop: Optional[Kop] = None
        self.content: List[Union["Divisie", Divisietekst]] = []

    def consume_children(self, children: List[Any]):
        for element in children:
            if isinstance(element, Tag):
                print(f"Tag: {element.name}")
                self.consume_tag(element)
            elif isinstance(element, NavigableString):
                print(f"String: {element}")
                self.consume_string(element)
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

    def consume_tag(self, tag: Tag): 
        # Headings will be send to the Kop
        if tag.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            if self.kop is not None:
                # @todo: shall return new divisie-tekst and the title set
                raise RuntimeError("Double titles are not implemented yet")
            kop = Kop()
            kop.consume_children(tag.children)
            self.kop = kop
            return
        
        # If the tag is a div then we will create a new Divisietekst
        elif tag.name == "div":
            content: Divisietekst = Divisietekst()
            content.consume_tag(tag)
            self.content.append(content)
            return

        # Else we will let the last Divisietekst consume the tag
        else:
            # If we do not have an "active Divisietekst" then we will create one
            content: Divisietekst = self._get_active_divisietekst()
            content: Divisietekst = Divisietekst()
            content.consume_tag(tag)

    def consume_string(self, string: NavigableString):
        pass

    def _get_active_divisietekst(self):
        # No content at all
        if not len(self.content):
            content: Divisietekst = Divisietekst()
            self.content.append(content)
            return content
        
        # Last content is divisietekst
        last_content = self.content[-1]
        if isinstance(last_content, Divisietekst):
            return last_content
        
        # Last content is not divisietekst, therefor we make one
        content: Divisietekst = Divisietekst()
        self.content.append(content)
        return content


def handle_tag(tag: Tag):
    pass


soup = BeautifulSoup(html_content, "html.parser")

root_divisie = Divisie()
root_divisie.consume_children(soup.children)

a = True



