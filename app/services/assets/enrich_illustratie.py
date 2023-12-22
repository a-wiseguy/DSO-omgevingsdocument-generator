from lxml import etree


def middleware_clean_attribute(xml_data: str, attribute: str) -> str:
    root = etree.fromstring(xml_data)
    for element in root.xpath(f"//*[@{attribute}]"):
        element.attrib.pop(attribute)

    output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
    return output


def middleware_clean_attributes(xml_data: str) -> str:
    xml_data = middleware_clean_attribute(xml_data, "data-hint-location")
    xml_data = middleware_clean_attribute(xml_data, "data-hint-object-code")
    return xml_data
