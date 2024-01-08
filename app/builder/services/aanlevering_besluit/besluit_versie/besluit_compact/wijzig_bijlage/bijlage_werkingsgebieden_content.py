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

        # TODO: add wid prefix in state
        org_id = self._state_manager.input_data.publication_settings.provincie_id
        expression = self._state_manager.input_data.publication_settings.besluit_frbr.expression
        expression_version = expression.split(";")[-1].strip()

        ewid_service = EWIDService(
            state_manager=self._state_manager,
            wid_prefix=f"{org_id}_{expression_version}",
        )
        content = ewid_service.modify_xml(xml_source=content)

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
