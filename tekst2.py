from abc import ABC, abstractmethod
from typing import Any, List, Optional, Union
from bs4 import BeautifulSoup, CData, Comment, Declaration, Doctype, NavigableString, ProcessingInstruction, Tag
import roman

from data import html_content


html_content = """
<h1>Title with a <em>bold</em> piece of text</h1>
<p>Line 1</p>
<p>Text with <em>important</em> parts</p>
<ul>
    <li><p>First un ordered list item</p></li>
    <li><p><em>Second</em> un ordered list item</p></li>
</ul>
<p>We might have more!</p>
<ol>
    <li><p>First ordered list item</p></li>
    <li><p><em>Second</em> ordered list item</p></li>
    <li>
        <ol>
            <li><p>Deeper list item 1!</p></li>
            <li><p>Deeper list item 2!</p></li>
            <li><p>Deeper list item 3!</p></li>
            <li><p>Deeper list item 4!</p></li>
            <li><p>Deeper list item 5!</p></li>
            <li>
                <ol>
                    <li><p>Very deep list item 1!</p></li>
                    <li><p>Very deep list item 2!</p></li>
                    <li><p>Very deep list item 3!</p></li>
                    <li><p>Very deep list item 4!</p></li>
                    <li><p>Very deep list item 5!</p></li>
                </ol>
            </li>
        </ol>
    </li>
</ol>
"""

expected_output = """
<Divisie>
    <Kop>
        <Opschrift>Title with a <i>bold</i> piece of text</Opschrift>
    </Kop>
    <Divisietekst>
        <Inhoud>
            <Al>Line 1</Al>
            <Al>Text with <i>important</i> parts</Al>
            <Lijst type="ongemarkeerd">
                <Li><Al>First un ordered list item</Al></Li>
                <Li><Al><i>Second</i> un ordered list item</Al></Li>
            </Lijst>
            <Al>We might have more!</Al>
        </Inhoud>
    </Divisietekst>
</Divisie>
"""



class I:
    def __init__(self):
        self.contents: List[Union[str, B]] = []

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
        if tag.name == "b":
            content = B()
            content.consume_children(tag.children)
            self.contents.append(content)

    def consume_string(self, string: NavigableString):
        self.contents.append(str(string))

    def as_xml(self, soup: BeautifulSoup) -> Tag:
        tag: Tag = soup.new_tag("i")
        for content in self.contents:
            if hasattr(content, 'as_xml'):
                child = content.as_xml(soup)
                tag.append(child)
            elif isinstance(content, str):
                tag.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")
        
        return tag


class B:
    def __init__(self):
        self.contents: List[Union[str, I]] = []

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
            self.contents.append(content)

    def consume_string(self, string: NavigableString):
        self.contents.append(str(string))

    def as_xml(self, soup: BeautifulSoup) -> Tag:
        tag: Tag = soup.new_tag("b")
        for content in self.contents:
            if hasattr(content, 'as_xml'):
                child = content.as_xml(soup)
                tag.append(child)
            elif isinstance(content, str):
                tag.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")
        
        return tag




class U:
    def __init__(self):
        self.contents: List[Union[str, I, B]] = []

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
            self.contents.append(content)
        if tag.name in ["b"]:
            content = B()
            content.consume_children(tag.children)
            self.contents.append(content)

    def consume_string(self, string: NavigableString):
        self.contents.append(str(string))

    def as_xml(self, soup: BeautifulSoup) -> Tag:
        tag: Tag = soup.new_tag("i")
        for content in self.contents:
            if hasattr(content, 'as_xml'):
                child = content.as_xml(soup)
                tag.append(child)
            elif isinstance(content, str):
                tag.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")
        
        return tag





class Sub:
    def __init__(self):
        self.contents: List[Union[str, I, B]] = []

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
            self.contents.append(content)
        if tag.name in ["b"]:
            content = B()
            content.consume_children(tag.children)
            self.contents.append(content)

    def consume_string(self, string: NavigableString):
        self.contents.append(str(string))

    def as_xml(self, soup: BeautifulSoup) -> Tag:
        tag: Tag = soup.new_tag("sub")
        for content in self.contents:
            if hasattr(content, 'as_xml'):
                child = content.as_xml(soup)
                tag.append(child)
            elif isinstance(content, str):
                tag.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")
        
        return tag


class Sup:
    def __init__(self):
        self.contents: List[Union[str, I, B]] = []

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
            self.contents.append(content)
        if tag.name in ["b"]:
            content = B()
            content.consume_children(tag.children)
            self.contents.append(content)

    def consume_string(self, string: NavigableString):
        self.contents.append(str(string))

    def as_xml(self, soup: BeautifulSoup) -> Tag:
        tag: Tag = soup.new_tag("sup")
        for content in self.contents:
            if hasattr(content, 'as_xml'):
                child = content.as_xml(soup)
                tag.append(child)
            elif isinstance(content, str):
                tag.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")
        
        return tag




class Strong:
    def __init__(self):
        self.contents: List[Union[str, I, B]] = []

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
            self.contents.append(content)
        if tag.name in ["b"]:
            content = B()
            content.consume_children(tag.children)
            self.contents.append(content)

    def consume_string(self, string: NavigableString):
        self.contents.append(str(string))

    def as_xml(self, soup: BeautifulSoup) -> Tag:
        tag: Tag = soup.new_tag("strong")
        for content in self.contents:
            if hasattr(content, 'as_xml'):
                child = content.as_xml(soup)
                tag.append(child)
            elif isinstance(content, str):
                tag.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")
        
        return tag





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

    def as_xml(self, soup: BeautifulSoup) -> Tag:
        tag_kop: Tag = soup.new_tag("Kop")
        tag_opschrift: Tag = soup.new_tag("Opschrift")
        tag_kop.append(tag_opschrift)

        for content in self.opschrift:
            if hasattr(content, 'as_xml'):
                child = content.as_xml(soup)
                tag_opschrift.append(child)
            elif isinstance(content, str):
                tag_opschrift.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")
        
        return tag_kop


class Al:
    def __init__(self):
        self.contents: List[Union[str, I]] = []

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
            self.contents.append(content)

    def consume_string(self, string: NavigableString):
        self.contents.append(str(string))

    def as_xml(self, soup: BeautifulSoup) -> Tag:
        tag: Tag = soup.new_tag("Al")
        for content in self.contents:
            if hasattr(content, 'as_xml'):
                child = content.as_xml(soup)
                tag.append(child)
            elif isinstance(content, str):
                tag.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")
        
        return tag


class NumberingStrategy:
    @abstractmethod
    def get(self, n: int) -> str:
        pass


class IntNumberingStragegy:
    def get(self, n: int) -> str:
        return str(n)


class Base26NumberingStragegy:
    def get(self, n: int) -> str:
        value = ""
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            value = chr(65 + remainder) + value
        return value.lower()


class RomanNumberingStrategy:
    def get(self, n: int) -> str:
        return roman.toRoman(n)


class NumberingFactory:
    def __init__(self, strategies: List[NumberingStrategy]):
        self._strategies: List[NumberingStrategy] = strategies
    
    def get_next(self, current_strategy: Optional[NumberingStrategy] = None) -> NumberingStrategy:
        if not self._strategies:
            raise RuntimeError("No numbering strategies registered")
        
        if current_strategy is None:
            return self._strategies[0]

        if not current_strategy in self._strategies:
            return self._strategies[0]
        
        current_index: int = self._strategies.index(current_strategy)
        next_index: int = (current_index + 1) % len(self._strategies)
        new_strategy: NumberingStrategy = self._strategies[next_index]
        return new_strategy


numbering_factory: NumberingFactory = NumberingFactory([
    IntNumberingStragegy(),
    Base26NumberingStragegy(),
    RomanNumberingStrategy(),
])



class LijstType(ABC):
    def has_number(self) -> bool:
        return False
    
    def get_number(self, n: int) -> str:
        return ""
    
    def get_numbering_strategy(self) -> Optional[NumberingStrategy]:
        return None
    
    @abstractmethod
    def get_type(self) -> str:
        pass


class LijstTypeUnordered(LijstType):
    def get_type(self) -> str:
        return "ongemarkeerd"


class LijstTypeOrdered(LijstType):
    def __init__(self, numbering_strategy: NumberingStrategy):
        self._numbering_strategy: NumberingStrategy = numbering_strategy

    def has_number(self) -> bool:
        return True
    
    def get_number(self, n: int) -> str:
        number: str = self._numbering_strategy.get(n)
        return f"{number}."
    
    def get_numbering_strategy(self) -> Optional[NumberingStrategy]:
        return self._numbering_strategy
    
    def get_type(self) -> str:
        return "expliciet"


class Li:
    def __init__(self, lijst_type: LijstType, idx: int):
        self.contents: List[Union[Al, Lijst]] = []
        self.lijst_type: LijstType = lijst_type
        self.idx: int = idx

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
        if tag.name == "p":
            element: Al = Al()
            element.consume_children(tag.children)
            self.contents.append(element)
        elif tag.name == "ul":
            element: Lijst = Lijst(LijstTypeUnordered())
            element.consume_children(tag.children)
            self.contents.append(element)
        elif tag.name == "ol":
            current_strategy: Optional[NumberingStrategy] = self.lijst_type.get_numbering_strategy()
            next_strategy: NumberingStrategy = numbering_factory.get_next(current_strategy)
            element: Lijst = Lijst(LijstTypeOrdered(next_strategy))
            element.consume_children(tag.children)
            self.contents.append(element)
        else:
            raise RuntimeError(f"Unsupport tag {tag.name} for Li")

    def consume_string(self, string: NavigableString):
        raw: str = str(string).strip()
        if len(raw) == 0:
            return

        al: Al = Al()
        al.consume_string(string)
        self.contents.append(al)

    def as_xml(self, soup: BeautifulSoup) -> Tag:
        tag_li: Tag = soup.new_tag("Li")
        if self.lijst_type.has_number():
            nummer: str = self.lijst_type.get_number(self.idx)

            tag_li_nummer: Tag = soup.new_tag("LiNummer")
            tag_li_nummer.append(nummer)

            tag_li.append(tag_li_nummer)

        for content in self.contents:
            if hasattr(content, 'as_xml'):
                child = content.as_xml(soup)
                tag_li.append(child)
            elif isinstance(content, str):
                tag_li.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")
        
        return tag_li


class Lijst:
    def __init__(self, lijst_type: LijstType):
        self.contents: List[Li] = []
        self.lijst_type: LijstType = lijst_type

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
        if tag.name == "li":
            content = Li(self.lijst_type, len(self.contents) + 1)
            content.consume_children(tag.children)
            self.contents.append(content)
        else:
            raise RuntimeError(f"Unsupported tag {tag.name} for Lijst")

    def consume_string(self, string: NavigableString):
        raw: str = str(string).strip()
        if len(raw) != 0:
            raise RuntimeError(f"Can not write plain text to Lijst. Trying to write: {raw}")

    def as_xml(self, soup: BeautifulSoup) -> Tag:
        attributes: dict = {
            "type": self.lijst_type.get_type()
        }
        tag: Tag = soup.new_tag("Lijst", **attributes)
        for content in self.contents:
            if hasattr(content, 'as_xml'):
                child = content.as_xml(soup)
                tag.append(child)
            elif isinstance(content, str):
                tag.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")
        
        return tag


class Inhoud:
    def __init__(self):
        # @todo add more see https://koop.gitlab.io/STOP/standaard/1.3.0/tekst_xsd_Element_tekst_Inhoud.html#Inhoud
        self.content_1: List[Union[Al, Lijst]] = [] # mgBlocksMinimaal
        # self.content_2: List[Al] # mgBlocksVolledig

    def consume_tag(self, tag: Tag):
        # Headings will be send to the Kop
        if tag.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            raise RuntimeError("Tussenkop not implemented yet")
        elif tag.name == "p":
            element: Al = Al()
            element.consume_children(tag.children)
            self.content_1.append(element)
        elif tag.name == "ul":
            element: Lijst = Lijst(LijstTypeUnordered())
            element.consume_children(tag.children)
            self.content_1.append(element)
        elif tag.name == "ol":
            element: Lijst = Lijst(LijstTypeOrdered(numbering_factory.get_next()))
            element.consume_children(tag.children)
            self.content_1.append(element)
        else:
            raise RuntimeError(f"Unsupport tag {tag.name}")

    def consume_string(self, string: NavigableString):
        pass

    def as_xml(self, soup: BeautifulSoup) -> Tag:
        tag: Tag = soup.new_tag("Inhoud")
        for content in self.content_1:
            if hasattr(content, 'as_xml'):
                child = content.as_xml(soup)
                tag.append(child)
            elif isinstance(content, str):
                tag.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")
        
        return tag



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
        if self.inhoud is None:
            self.inhoud = Inhoud()
        
        return self.inhoud

    def as_xml(self, soup: BeautifulSoup) -> Tag:
        tag_divisietekst: Tag = soup.new_tag("Divisietekst")

        if self.kop is not None:
            tag_kop: Tag = self.kop.as_xml(soup)
            tag_divisietekst.append(tag_kop)

        if self.inhoud is not None:
            tag_inhoud: Tag = self.inhoud.as_xml(soup)
            tag_divisietekst.append(tag_inhoud)

        return tag_divisietekst


class Divisie:
    def __init__(self):
        self.kop: Optional[Kop] = None
        self.contents: List[Union["Divisie", Divisietekst]] = []

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
            self.contents.append(content)
            return

        # Else we will let the last Divisietekst consume the tag
        else:
            # If we do not have an "active Divisietekst" then we will create one
            content: Divisietekst = self._get_active_divisietekst()
            content.consume_tag(tag)
            a = True

    def consume_string(self, string: NavigableString):
        pass

    def _get_active_divisietekst(self):
        # No content at all
        if not len(self.contents):
            content: Divisietekst = Divisietekst()
            self.contents.append(content)
        
        # Last content is not a divisietekst
        last_content = self.contents[-1]
        if not isinstance(last_content, Divisietekst):
            content: Divisietekst = Divisietekst()
            self.contents.append(content)
        
        # Return the last which is now forced to be a Divisietekst
        return self.contents[-1]

    def as_xml(self, soup: BeautifulSoup) -> Tag:
        tag_divisie: Tag = soup.new_tag("Divisie")

        if self.kop is not None:
            tag_kop: Tag = self.kop.as_xml(soup)
            tag_divisie.append(tag_kop)

        for content in self.contents:
            if hasattr(content, 'as_xml'):
                child = content.as_xml(soup)
                tag_divisie.append(child)
            elif isinstance(content, str):
                tag_divisie.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")

        return tag_divisie


def handle_tag(tag: Tag):
    pass


soup = BeautifulSoup(html_content, "html.parser")

root_divisie = Divisie()
root_divisie.consume_children(soup.children)

soup = BeautifulSoup(features='xml')
xml = root_divisie.as_xml(soup)

a = True






