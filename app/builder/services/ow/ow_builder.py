from typing import List
from uuid import UUID
from app.builder.services import BuilderService
from app.builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied import (
    Werkingsgebied,
)
from app.builder.state_manager.models import OutputFile, StrContentData
from app.builder.state_manager.state_manager import StateManager
from app.models import ContentType
from app.services.ow.models import (
    Annotation,
    OWDivisie,
    OWDivisieTekst,
    OWGebied,
    OWGebiedenGroep,
    OWTekstDeel,
)
from app.services.utils.helpers import load_template


class OwBuilder(BuilderService):
    """
    The OwBuilder class is responsible for building IMOW related objects
    and generating output files in XML format.

    Builds: OWGebied, OWGebiedenGroep, OWDivisie, OWDivisieTekst, OWTekstDeel for annotating policy.
    """

    def apply(self, state_manager: StateManager) -> StateManager:
        """
        Create all ow objects and save the output files to state
        """
        werkingsgebieden = state_manager.input_data.resources.werkingsgebied_repository.all()
        leveringid = state_manager.input_data.publication_settings.opdracht.id_levering

        locaties_data = self._build_locaties_data(
            werkingsgebieden=werkingsgebieden,
            object_tekst_lookup=state_manager.object_tekst_lookup,
            levering_id=leveringid,
        )
        locaties_file = self._create_locatie_file(locaties_data)

        divisie_data = self._build_divisies_data(
            object_tekst_lookup=state_manager.object_tekst_lookup,
            levering_id=leveringid,
        )
        divisies_file = self._create_divisie_file(divisie_data)

        manifest_file = self._create_manifest_file(
            act_akn=str(state_manager.input_data.publication_settings.regeling_frbr.work),
            doel=state_manager.input_data.publication_settings.doel,
        )

        regelinggebied_file = self._create_regelinggebied_file(levering_id=leveringid)

        state_manager.add_output_file(locaties_file)
        state_manager.add_output_file(divisies_file)
        state_manager.add_output_file(manifest_file)
        state_manager.add_output_file(regelinggebied_file)

        return state_manager

    def _create_locatie_file(self, locaties_data):
        content = load_template(
            "templates/ow/owLocaties.xml",
            pretty_print=True,
            data=locaties_data,
        )
        output_file = OutputFile(
            filename="owLocaties.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file

    def _create_divisie_file(self, divisie_data):
        content = load_template(
            "templates/ow/owDivisie.xml",
            pretty_print=True,
            data=divisie_data,
        )
        output_file = OutputFile(
            filename="owDivisie.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file

    def _create_regelinggebied_file(self, levering_id) -> OutputFile:
        content = load_template(
            "templates/ow/owRegelingsgebied.xml",
            pretty_print=True,
            levering_id=levering_id,
        )
        output_file = OutputFile(
            filename="owRegelingsgebied.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file

    def _create_manifest_file(self, act_akn, doel):
        doel: str = f"/join/id/proces/pv28/{doel.jaar}/{doel.naam}"
        content = load_template(
            "templates/ow/manifest-ow.xml",
            pretty_print=True,
            data={"act_akn": act_akn, "doel_id": doel},
        )
        output_file = OutputFile(
            filename="manifest-ow.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file

    def _build_locaties_data(
        self, werkingsgebieden: List[Werkingsgebied], object_tekst_lookup, levering_id
    ) -> OutputFile:
        """
        Create OWGebied and OWGebiedenGroep objects and return them in a dict
        """
        xml_data = {
            "leveringsId": levering_id,
            "objectTypen": ["Ambtsgebied"],
            "gebiedengroepen": [],
            "gebieden": [],
        }
        # Create new OW Locations
        for werkingsgebied in werkingsgebieden:
            ow_locations = [
                OWGebied(geo_uuid=loc.UUID, noemer=loc.Title) for loc in werkingsgebied.Locaties
            ]
            ow_group = OWGebiedenGroep(
                geo_uuid=werkingsgebied.UUID,
                noemer=werkingsgebied.Title,
                locations=ow_locations,
            )
            xml_data["gebieden"].extend(ow_locations)
            xml_data["gebiedengroepen"].append(ow_group)

        # extend object types if needed
        if len(xml_data["gebieden"]) > 0:
            xml_data["objectTypen"].append("Gebied")
        if len(xml_data["gebiedengroepen"]) > 0:
            xml_data["objectTypen"].append("Gebiedengroep")

        ow_gebied_mapping = {gebied.geo_uuid: gebied.OW_ID for gebied in xml_data["gebieden"]}
        ow_gebied_mapping.update(
            {
                gebiedengroep.geo_uuid: gebiedengroep.OW_ID
                for gebiedengroep in xml_data["gebiedengroepen"]
            }
        )
        for object_code, values in object_tekst_lookup.items():
            # Find the matching OWGebied and update ow_location_id to the state
            matching_ow_gebied = ow_gebied_mapping.get(UUID(values["gebied_uuid"]))
            if matching_ow_gebied:
                values["ow_location_id"] = matching_ow_gebied

        return xml_data

    def _build_divisies_data(self, object_tekst_lookup, levering_id):
        """
        Create OWDivisie and OWTekstDeel objects and return them in a dict 
        """
        xml_data = {
            "leveringsId": levering_id,
            "objectTypen": [],
            "annotaties": [],
        }

        for object_code, values in object_tekst_lookup.items():
            if not values["gebied_uuid"]:
                continue

            if values["tag"] == "Divisietekst":
                xml_data["objectTypen"].append("Divisietekst")
                xml_data["objectTypen"].append("Tekstdeel")
                ow_div = OWDivisieTekst(wid=values["wid"])
                ow_text = OWTekstDeel(divisie=ow_div.OW_ID, locations=[values["ow_location_id"]])

            if values["tag"] == "Divisie":
                xml_data["objectTypen"].append("Divisie")
                xml_data["objectTypen"].append("Tekstdeel")
                ow_div = OWDivisie(wid=values["wid"])
                ow_text = OWTekstDeel(divisie=ow_div.OW_ID, locations=[values["ow_location_id"]])

            new_annotation = Annotation(divisie=ow_div, tekstdeel=ow_text)
            xml_data["annotaties"].append(new_annotation)

        xml_data["objectTypen"] = list(set(xml_data["objectTypen"]))

        return xml_data
