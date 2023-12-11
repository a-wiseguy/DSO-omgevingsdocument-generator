import re
import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.models import FRBR


class Locatie(BaseModel):
    Object_ID: Optional[int] = Field(None)
    Object_Code: Optional[str] = Field(None)
    UUID: uuid.UUID
    Title: str
    Symbol: str
    Created_Date: datetime
    Modified_Date: datetime
    Geometry: str


class Werkingsgebied(BaseModel):
    Object_ID: Optional[int] = Field(None)
    Object_Code: Optional[str] = Field(None)
    UUID: uuid.UUID
    Title: str
    Symbol: str
    Created_Date: datetime
    Modified_Date: datetime
    Achtergrond_Verwijzing: str
    Achtergrond_Actualiteit: str
    Locaties: List[Locatie] = Field(..., alias="Onderverdelingen")

    def get_FRBR(self, provincie_id: str, expression_taal: str) -> FRBR:
        identifier: str = self.get_identifier()
        work_datum: str = f"{self.Created_Date.year}"
        work: str = f"/join/id/regdata/{provincie_id}/{work_datum}/{identifier}"

        version: str = self.get_version(expression_taal)
        expression: str = f"{work}/{version}"

        return FRBR(
            work=work,
            expression=expression,
        )

    def get_identifier(self) -> str:
        s: str = self.Title.lower()
        s = re.sub(r"[^a-z0-9 ]+", "", s)
        s = s.replace(" ", "-")
        return s

    def get_version(self, expression_taal: str) -> str:
        date_version: str = self.Modified_Date.strftime("%Y-%m-%d;%H%M")
        version: str = f"{self}@{date_version}"
        return version

    def get_gml_filename(self) -> str:
        return f"locaties_{self.get_identifier()}.gml"

    def get_gml_filepath(self) -> str:
        return f"output/{self.get_gml_filename()}"

    def get_gio_filename(self) -> str:
        return f"GIO_locaties_{self.get_identifier()}.xml"

    def get_gio_filepath(self) -> str:
        return f"output/{self.get_gio_filename()}"
