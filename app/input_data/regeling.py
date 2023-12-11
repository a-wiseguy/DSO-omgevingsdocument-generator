from pydantic import BaseModel


class Regeling(BaseModel):
    versienummer: str
    officiele_titel: str
    citeertitel: str
    is_officieel: bool
