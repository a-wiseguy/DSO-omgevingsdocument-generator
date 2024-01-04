from dataclasses import dataclass
from typing import List, Optional


class OWStateRepository:
    def __init__(self):
        self.locaties_content = None
        self.divisie_content = None
        self.regelingsgebied_content = None

    def store_locaties_content(self, xml_data):
        self.locaties_content = xml_data

    def store_divisie_content(self, xml_data):
        self.divisie_content = xml_data

    def store_regelingsgebied_content(self, xml_data):
        self.regelingsgebied_content = xml_data

    def get_location_objecttypes(self):
        return self.locaties_content.get("objectTypen", [])

    def get_divisie_objecttypes(self):
        return self.divisie_content.get("objectTypen", [])

    def get_regelingsgebied_objecttypes(self):
        return self.regelingsgebied_content.get("objectTypen", [])

