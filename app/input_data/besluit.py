from typing import List

from pydantic import BaseModel


class Artikel(BaseModel):
    label: str
    nummer: str
    inhoud: str


class Besluit(BaseModel):
    officiele_titel: str
    regeling_opschrift: str
    aanhef: str
    wijzig_artikel: Artikel
    artikelen: List[Artikel]
    sluiting: str
    ondertekening: str
