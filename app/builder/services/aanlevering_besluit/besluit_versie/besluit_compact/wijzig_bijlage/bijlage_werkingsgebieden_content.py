from typing import List

from lxml import etree

from app.builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied import Werkingsgebied
from app.builder.state_manager.state_manager import StateManager
from app.services.ewid.ewid_service import EWIDService
from app.services.utils.helpers import load_template


class BijlageWerkingsgebiedenContent:
    def __init__(self, state_manager: StateManager):
        self._state_manager: StateManager = state_manager

    def create(self) -> str:
        werkingsgebieden: List[
            Werkingsgebied
        ] = self._state_manager.input_data.resources.werkingsgebied_repository.all()

        content = load_template(
            "templates/akn/besluit_versie/besluit_compact/wijzig_bijlage/BijlageWerkingsgebieden.xml",
            werkingsgebieden=werkingsgebieden,
        )

        # @TODO: De gegenereerde eid/wid zijn niet goed.
        # Zie onderaan deze pagina
        ewid_service = EWIDService(xml_string=content)
        content = ewid_service.fill_ewid()

        # Resolve the wid from the werkingsgebieden
        content = self._create_werkingsgebieden_wid_lookup(content)

        return content

    def _create_werkingsgebieden_wid_lookup(self, xml_content: str):
        root = etree.fromstring(xml_content)
        elements = root.xpath("//*[@data-info-werkingsgebied-uuid]")

        for element in elements:
            uuid = element.get("data-info-werkingsgebied-uuid")
            eid = element.get("eId")
            # Set the werkingsgebied eid in the StateManager
            self._state_manager.werkingsgebied_eid_lookup[uuid] = eid
            del element.attrib["data-info-werkingsgebied-uuid"]

        return etree.tostring(root, encoding="unicode", pretty_print=True)


"""

Ik moet krijgen iets als dit:

<Bijlage eId="cmp_A" wId="pv28_1__cmp_A">
    <Kop>
        <Label>Bijlage</Label>
        <Nummer>A</Nummer>
        <Opschrift>Overzicht informatieobjecten</Opschrift>
    </Kop>
    <Divisietekst eId="cmp_A__content_o_1"
        wId="pv28_1__cmp_A__content_o_1">
        <Inhoud>
            <Begrippenlijst eId="cmp_A__content_o_1__list_1"
                wId="pv28_1__cmp_A__content_o_1__list_1">
                <Begrip eId="cmp_A__content_o_1__list_1__item_1"
                    wId="pv28_1__cmp_A__content_o_1__list_1__item_1">
                    <Term>Maatwerkgebied glastuinbouw</Term>
                    <Definitie>
                        <Al>
                            <ExtIoRef
                                eId="cmp_A__content_o_1__list_1__item_1__ref_o_1"
                                ref="/join/id/regdata/pv28/2023/maatwerkgebied-glastuinbouw/nld@2023-03-15;0000"
                                wId="pv28_1__cmp_A__content_o_1__list_1__item_1__ref_o_1">/join/id/regdata/pv28/2023/maatwerkgebied-glastuinbouw/nld@2023-03-15;0000</ExtIoRef>
                        </Al>
                    </Definitie>
                </Begrip>
            </Begrippenlijst>
        </Inhoud>
    </Divisietekst>
</Bijlage>

"""

"""

Maar ik krijg:

<Bijlage eId="cmp_o_1" wId="pv28_0000__cmp_o_1">
    <Kop>
        <Label>Bijlage</Label>
        <Nummer>A</Nummer>
        <Opschrift>Overzicht informatieobjecten</Opschrift>
    </Kop>
    <Divisietekst eId="cmp_o_1__content_o_1" wId="pv28_0000__cmp_o_1__content">
        <Inhoud>
        <Begrippenlijst eId="list_o_1_o_1" wId="pv28_0000__list_o_1">
            <Begrip eId="list_o_1__item_o_1" wId="pv28_0000__list_o_1__item">
            <Term>Maatwerkgebied glastuinbouw</Term>
            <Definitie>
                <Al>
                    <ExtIoRef ref="/join/id/regdata/pv28/2022/maatwerkgebied-glastuinbouw/nld@2022-03-15;0000" eId="ref_o_1_o_1" wId="pv28_0000__ref_o_1">/join/id/regdata/pv28/2022/maatwerkgebied-glastuinbouw/nld@2022-03-15;0000</ExtIoRef>
                </Al>
            </Definitie>
            </Begrip>
        </Begrippenlijst>
        </Inhoud>
    </Divisietekst>
</Bijlage>

Belangrijke punten zijn:
- <Bijlage eId="cmp_o_1" wId="pv28_0000__cmp_o_1"> Dit moeten we kunnen prefixen als iets, hier als cmp_A bovenop de wid-prefix
- Weten we zeker dat de eid/wid van de ExtIoRef goed genoeg is?

"""
