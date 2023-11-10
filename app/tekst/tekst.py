from abc import ABCMeta, abstractmethod
from typing import Any, List, Optional, Type, Union

from bs4 import BeautifulSoup, CData, Comment, Declaration, Doctype, NavigableString, ProcessingInstruction, Tag

from app.tekst.lijst import LijstType, LijstTypeOrdered, LijstTypeUnordered, NumberingStrategy, numbering_factory


class AsXmlTrait(metaclass=ABCMeta):
    @abstractmethod
    def as_xml(self, soup: BeautifulSoup) -> Union[Tag, str]:
        pass


class Element(AsXmlTrait, metaclass=ABCMeta):
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

    @abstractmethod
    def consume_tag(self, tag: Tag):
        pass

    @abstractmethod
    def consume_string(self, string: NavigableString):
        pass


class ElementGenerator(metaclass=ABCMeta):
    def can_consume_tag(self, tag: Tag) -> bool:
        pass

    def generate(self, tag: Tag, context: dict = {}) -> Element:
        pass


class SimpleElement(Element, metaclass=ABCMeta):
    element_generators: List[ElementGenerator] = []

    def __init__(self, xml_tag_name: str = ""):
        self.contents: List[Union[Element, str]] = []
        self.xml_tag_name: str = xml_tag_name

    def consume_tag(self, tag: Tag):
        for element_generator in self.element_generators:
            if not element_generator.can_consume_tag(tag):
                continue
            content: Element = element_generator.generate(
                tag=tag,
                context=self._get_generate_context(),
            )
            content.consume_children(tag.children)
            self.contents.append(content)
            return
        raise RuntimeError("Can not consume tag")

    def consume_string(self, string: NavigableString):
        self.contents.append(str(string))

    def as_xml(self, soup: BeautifulSoup, tag_name_overwrite: Optional[str] = None) -> Union[Tag, str]:
        tag_name: str = tag_name_overwrite if tag_name_overwrite is not None else self.xml_tag_name
        tag: Tag = soup.new_tag(tag_name)
        for content in self.contents:
            if hasattr(content, 'as_xml'):
                child = content.as_xml(soup)
                tag.append(child)
            elif isinstance(content, str):
                tag.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")

        return tag

    def _get_generate_context(self) -> dict:
        return {}


class SimpleGenerator(ElementGenerator):
    def __init__(self, tag_name: str, class_type: Type[SimpleElement]):
        self._tag_name: str = tag_name
        self._class_type: Type[SimpleElement] = class_type

    def can_consume_tag(self, tag: Tag) -> bool:
        return tag.name == self._tag_name

    def generate(self, tag: Tag, context: dict = {}) -> Element:
        element = self._class_type(tag)
        return element


class OrderedLijstGenerator(ElementGenerator):
    def can_consume_tag(self, tag: Tag) -> bool:
        return tag.name ==  "ol"

    def generate(self, tag: Tag, context: dict = {}) -> Element:
        current_strategy: Optional[NumberingStrategy] = context.get("current_strategy", None)
        next_strategy: NumberingStrategy = numbering_factory.get_next(current_strategy)
        element = Lijst(
            tag=tag,
            lijst_type=LijstTypeOrdered(next_strategy),
        )
        return element


class UnorderedLijstGenerator(ElementGenerator):
    def can_consume_tag(self, tag: Tag) -> bool:
        return tag.name ==  "ul"

    def generate(self, tag: Tag, context: dict = {}) -> Element:
        element = Lijst(
            tag=tag,
            lijst_type=LijstTypeUnordered(),
        )
        return element


class LiGenerator(ElementGenerator):
    def can_consume_tag(self, tag: Tag) -> bool:
        return tag.name ==  "li"

    def generate(self, tag: Tag, context: dict = {}) -> Element:
        lijst_type: Optional[LijstType] = context.get("lijst_type", None)
        if lijst_type is None:
            raise RuntimeError("Missing required context LijstType to create a Li")
        idx: Optional[int] = context.get("idx", None)
        if idx is None:
            raise RuntimeError("Missing required context idx to create a Li")
        element = Li(tag, lijst_type, idx)
        return element


class I(SimpleElement):
    def __init__(self, tag: Optional[Tag]):
        super().__init__(xml_tag_name="i")


class B(SimpleElement):
    def __init__(self, tag: Optional[Tag]):
        super().__init__(xml_tag_name="b")


class U(SimpleElement):
    def __init__(self, tag: Optional[Tag]):
        super().__init__(xml_tag_name="u")


class Sub(SimpleElement):
    def __init__(self, tag: Optional[Tag]):
        super().__init__(xml_tag_name="sub")


class Sup(SimpleElement):
    def __init__(self, tag: Optional[Tag]):
        super().__init__(xml_tag_name="sup")


class Strong(SimpleElement):
    def __init__(self, tag: Optional[Tag]):
        super().__init__(xml_tag_name="strong")


class Al(SimpleElement):
    def __init__(self, tag: Optional[Tag]):
        super().__init__(xml_tag_name="Al")

    def as_xml(self, soup: BeautifulSoup, tag_name_overwrite: Optional[str] = None) -> Union[Tag, str]:
        if not self.contents:
            return ""

        return SimpleElement.as_xml(self, soup=soup, tag_name_overwrite=tag_name_overwrite)


class Br(SimpleElement):
    def __init__(self, tag: Optional[Tag]):
        super().__init__(xml_tag_name="br")


class Kop(SimpleElement):
    def __init__(self, tag: Optional[Tag]):
        super().__init__()
    
    def as_xml(self, soup: BeautifulSoup) -> Union[Tag, str]:
        opschrift = SimpleElement.as_xml(self, soup=soup, tag_name_overwrite="Opschrift")
        kop: Tag = soup.new_tag("Kop")
        kop.append(opschrift)
        return kop


class Inhoud(SimpleElement):
    def __init__(self, tag: Optional[Tag]):
        super().__init__(xml_tag_name="Inhoud")


class Li(SimpleElement):
    def __init__(self, tag: Optional[Tag], lijst_type: LijstType, idx: int):
        super().__init__()
        self.lijst_type: LijstType = lijst_type
        self.idx: int = idx

    def consume_string(self, string: NavigableString):
        raw: str = str(string).strip()
        if len(raw) == 0:
            return

        al: Al = Al(tag=None)
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

    def _get_generate_context(self) -> dict:
        current_strategy: Optional[NumberingStrategy] = self.lijst_type.get_numbering_strategy()
        return {
            "current_strategy": current_strategy,
        }


class Lijst(SimpleElement):
    def __init__(self, tag: Optional[Tag], lijst_type: LijstType):
        super().__init__()
        self.lijst_type: LijstType = lijst_type

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
    
    def _get_generate_context(self) -> dict:
        return {
            "lijst_type": self.lijst_type,
            "idx": len(self.contents) + 1,
        }


class Divisietekst(Element):
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
    
    def consume_string(self, string: NavigableString):
        raw: str = str(string).strip()
        if len(raw) == 0:
            return
        raise RuntimeError(f"Consume string not implemented for Divisietekst")

    def _get_inhoud(self) -> Inhoud:
        if self.inhoud is None:
            self.inhoud = Inhoud(tag=None)
        
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


class Divisie(Element):
    def __init__(self):
        self.kop: Optional[Kop] = None
        self.contents: List[Union["Divisie", Divisietekst]] = []
    
    def consume_tag(self, tag: Tag): 
        # Headings will be send to the Kop
        if tag.name in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            if self.kop is not None:
                # @todo: shall return new divisie-tekst and the title set
                raise RuntimeError("Double titles are not implemented yet")
            kop = Kop(tag=None)
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

    def consume_string(self, string: NavigableString):
        raw: str = str(string).strip()
        if len(raw) == 0:
            return
        raise RuntimeError(f"Consume string not implemented for Divisie")

    def _get_active_divisietekst(self) -> Divisietekst:
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


element_i_handler = SimpleGenerator("i", I)
element_em_handler = SimpleGenerator("em", I)
element_b_handler = SimpleGenerator("b", B)
element_u_handler = SimpleGenerator("u", U)
element_sub_handler = SimpleGenerator("sub", Sub)
element_sup_handler = SimpleGenerator("sup", Sup)
element_strong_handler = SimpleGenerator("strong", Strong)
element_p_handler = SimpleGenerator("p", Al)
element_ul_handler = UnorderedLijstGenerator()
element_ol_handler = OrderedLijstGenerator()
element_li_handler = LiGenerator()
element_br_handler = SimpleGenerator("br", Br)


I.element_generators = [
    element_b_handler,
    element_u_handler,
    element_sub_handler,
    element_sup_handler,
    element_strong_handler,
    element_br_handler,
]
B.element_generators = [
    element_i_handler,
    element_em_handler,
    element_u_handler,
    element_sub_handler,
    element_sup_handler,
    element_strong_handler,
    element_br_handler,
]
U.element_generators = [
    element_i_handler,
    element_em_handler,
    element_b_handler,
    element_sub_handler,
    element_sup_handler,
    element_strong_handler,
    element_br_handler,
]
Sub.element_generators = [
]
Sup.element_generators = [
]
Strong.element_generators = [
    element_i_handler,
    element_em_handler,
    element_b_handler,
    element_u_handler,
    element_sub_handler,
    element_sup_handler,
    element_br_handler,
]
Al.element_generators = [
    element_i_handler,
    element_em_handler,
    element_b_handler,
    element_u_handler,
    element_sub_handler,
    element_sup_handler,
    element_strong_handler,
    element_br_handler,
]
Kop.element_generators = [
    element_i_handler,
    element_em_handler,
    element_b_handler,
    element_u_handler,
    element_sub_handler,
    element_sup_handler,
    element_strong_handler,
]
Inhoud.element_generators = [
    element_p_handler,
    element_ul_handler,
    element_ol_handler,
]
Li.element_generators = [
    element_p_handler,
    element_ul_handler,
    element_ol_handler,
]
Lijst.element_generators = [
    element_li_handler,
]
