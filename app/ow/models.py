from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from .enums import IMOWTYPES
from .ow_id import generate_ow_id


class OWObject(BaseModel):
    OW_ID: str


class OWLocation(OWObject):
    geo_uuid: UUID
    noemer: Optional[str] = None


class OWGebied(OWLocation):
    OW_ID: str = Field(default_factory=lambda: generate_ow_id(IMOWTYPES.GEBIED))


class OWGebiedenGroep(OWLocation):
    OW_ID: str = Field(default_factory=lambda: generate_ow_id(IMOWTYPES.GEBIEDENGROEP))
    locations: List[OWGebied] = []


class OWDivisieTekst(OWObject):
    OW_ID: str = Field(default_factory=lambda: generate_ow_id(IMOWTYPES.DIVISIETEKST))
    wid: str


class OWTekstDeel(OWObject):
    OW_ID: str = Field(default_factory=lambda: generate_ow_id(IMOWTYPES.TEKSTDEEL))
    divisie: str  # is divisie(tekst) OW_ID
    locations: List[str]  # OWlocation OW_ID list


class Annotation(BaseModel):
    divisie: OWDivisieTekst
    tekstdeel: OWTekstDeel
