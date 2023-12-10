from uuid import UUID

from lxml import etree

from app.assets.assets_service import Asset, AssetsService


def middleware_enrich_illustratie(assets_service: AssetsService, xml_data: str) -> str:
    parser = etree.XMLParser(remove_blank_text=False, encoding="utf-8")
    root = etree.fromstring(xml_data.encode("utf-8"), parser)
    illustrations = root.findall(".//Illustratie")
    for illustration in illustrations:
        asset_uuid: str = illustration.get("data-info-asset-uuid")
        if not asset_uuid:
            continue
        asset: Asset = assets_service.get(UUID(asset_uuid))
        illustration.set("breedte", str(asset.Meta.Breedte))
        illustration.set("dpi", str(asset.Meta.Dpi))
        illustration.set("formaat", asset.Meta.Formaat)
        illustration.set("hoogte", str(asset.Meta.Hoogte))
        illustration.set("naam", asset.get_filename())
        illustration.set("uitlijning", asset.Meta.Uitlijning)
        del illustration.attrib["data-info-asset-uuid"]

    output: str = etree.tostring(root, pretty_print=False, encoding="utf-8").decode("utf-8")
    return output


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
