from enum import Enum
from typing import List
from pydantic import BaseModel, Field

from utils.waardelijsten import ProcedureStappenDefinitief, ProcedureType


class FRBR(BaseModel):
    work: str
    expression: str


class BestuursDocument(BaseModel):
    eindverantwoordelijke: str
    maker: str
    soort_bestuursorgaan: str
    onderwerp: str
    rechtsgebied: str


class Besluit(BaseModel):
    frbr: FRBR
    bestuurs_document: BestuursDocument
    officiele_titel: str
    soort_procedure: ProcedureType
    informatieobject_refs: List[str] = Field([])


class Regeling(BaseModel):
    frbr: FRBR
    bestuurs_document: BestuursDocument
    versienummer: str
    officiele_titel: str
    citeertitel: str
    is_officieel: str


class ProcedureStap(BaseModel):
    soort_stap: ProcedureStappenDefinitief
    voltooid_op: str


class ProcedureVerloop(BaseModel):
    bekend_op: str
    stappen: List[ProcedureStap] = Field([])


class ContentType(str, Enum):
    GML = "application/gml+xml"
    XML = "application/xml"
    JPG = "image/jpeg"


class Bestand(BaseModel):
    bestandsnaam: str
    content_type: str

