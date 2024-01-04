from app.builder.state_manager.models import OutputFile, StrContentData
from app.models import ContentType
from app.services.ow.enums import OwDivisieObjectType
from app.services.ow.models import Annotation, OWDivisie, OWDivisieTekst, OWTekstDeel
from app.services.utils.helpers import load_template


class OwDivisieContent:
    """
    Prepares the content for the OWDivisies file from object_tekst_lookup.
    """

    def __init__(self, object_tekst_lookup, levering_id):
        self.object_tekst_lookup = object_tekst_lookup
        self.levering_id = levering_id
        self.xml_data = {
            "filename": "owDivisie.xml",
            "leveringsId": self.levering_id,
            "objectTypen": [],
            "annotaties": [],
        }
        self.file = None

    def create_divisies(self):
        """
        Create OWDivisie and OWTekstDeel objects and return them as output file
        """
        self._create_ow_divisies()
        self.file = self.create_file()
        return self.xml_data

    def _create_ow_divisies(self):
        """
        Create new OW Divisie annotations from locaties and
        policy objects using object_tekst_lookup.
        """
        for object_code, values in self.object_tekst_lookup.items():
            if not values["gebied_uuid"]:
                continue

            if values["tag"] == "Divisietekst":
                ow_div = OWDivisieTekst(wid=values["wid"])
                ow_text = OWTekstDeel(divisie=ow_div.OW_ID, locations=[values["ow_location_id"]])

                if OwDivisieObjectType.DIVISIETEKST.value not in self.xml_data["objectTypen"]:
                    self.xml_data["objectTypen"].append(OwDivisieObjectType.DIVISIETEKST.value)

            if values["tag"] == "Divisie":
                ow_div = OWDivisie(wid=values["wid"])
                ow_text = OWTekstDeel(divisie=ow_div.OW_ID, locations=[values["ow_location_id"]])

                if OwDivisieObjectType.DIVISIE.value not in self.xml_data["objectTypen"]:
                    self.xml_data["objectTypen"].append(OwDivisieObjectType.DIVISIE.value)

            new_annotation = Annotation(divisie=ow_div, tekstdeel=ow_text)
            self.xml_data["annotaties"].append(new_annotation)

            if OwDivisieObjectType.TEKSTDEEL.value not in self.xml_data["objectTypen"]:
                self.xml_data["objectTypen"].append(OwDivisieObjectType.TEKSTDEEL.value)

    def create_file(self):
        content = load_template(
            "templates/ow/owDivisie.xml",
            pretty_print=True,
            data=self.xml_data,
        )
        output_file = OutputFile(
            filename="owDivisie.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
