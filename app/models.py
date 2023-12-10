from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, root_validator

from utils.waardelijsten import ProcedureStappenDefinitief, ProcedureType, Provincie


class FRBR(BaseModel):
    work: str
    expression: str


class BestuursDocument(BaseModel):
    eindverantwoordelijke: str
    maker: str
    soort_bestuursorgaan: str
    onderwerp: str
    rechtsgebied: str


class Regeling(BaseModel):
    frbr: FRBR
    bestuurs_document: BestuursDocument
    versienummer: str
    officiele_titel: str
    citeertitel: str
    is_officieel: str


class WijzigArtikel(BaseModel):
    Label: str
    Nummer: str
    Wat: str


class Artikel(BaseModel):
    Label: str
    Nummer: str
    Inhoud: Optional[str]


class WijzigingBijlage(BaseModel):
    Label: str
    Nummer: str
    Opschrift: str


class BesluitCompact(BaseModel):
    RegelingOpschrift: str
    Aanhef: str
    WijzigArtikel: WijzigArtikel
    Artikelen: List[Artikel]
    WijzigingBijlage: WijzigingBijlage
    Sluiting: str
    Ondertekening: str


class Besluit(BaseModel):
    frbr: FRBR
    bestuurs_document: BestuursDocument
    officiele_titel: str
    soort_procedure: ProcedureType
    informatieobject_refs: List[str] = Field([])
    compact: BesluitCompact


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


class DSOVersion(BaseModel):
    STOP: str = "1.3.0"
    TPOD: str = "2.0.2"
    LVBB: str = "1.2.0"


class PublicatieOpdracht(BaseModel):
    is_validatie: bool = False
    id_levering: UUID = Field(default_factory=uuid4)
    id_bevoegdgezag: str = "00000001002306608000"  # own ids?
    id_aanleveraar: str = "00000003011411800000"  # own ids?
    publicatie: str  # filename
    datum_bekendmaking: str


class DocumentType(Enum):
    PROGRAMMA = "Omgevingsprogramma"
    VISIE = "Omgevingsvisie"


class PublicationSettings(BaseModel):
    document_type: DocumentType
    previous_akn_act: int
    previous_akn_bill: int
    public_release_date: str
    provincie_id: str = "pv28"
    provincie_ref: str = Provincie.Zuid_Holland.value  # "tooi/id/provincie/pv28"
    dso_versioning: DSOVersion = Field(default_factory=DSOVersion)

    @classmethod
    def from_json(cls, json_data):
        data = {
            "document_type": DocumentType[json_data["type"]],
            "previous_akn_act": json_data["ID"]["ACT"],
            "previous_akn_bill": json_data["ID"]["BILL"],
            "public_release_date": json_data["public_release_date"],
        }
        return cls(**data)

    @property
    def next_akn_id_bill(self):
        return self.previous_akn_bill + 1

    @property
    def next_akn_id_act(self):
        return self.previous_akn_bill + 1


class AKN(BaseModel):
    province_id: str = "pv28"
    previous_act: int
    previous_bill: int
    year: int = Field(default_factory=lambda: datetime.now().year)
    doel_id: str = None

    current_act: int = Field(init=False)
    current_bill: int = Field(init=False)

    @root_validator(pre=True, allow_reuse=True)
    def set_current_values(cls, values):
        values["current_act"] = values.get("previous_act", 0) + 1
        values["current_bill"] = values.get("previous_bill", 0) + 1
        return values

    def as_FRBR(self, akn_type: str = "bill") -> FRBR:
        if akn_type not in ["bill", "act"]:
            raise ValueError("Invalid AKN type. Must be 'bill' or 'act'.")

        base_akn = f"/akn/nl/{akn_type}/{self.province_id}/{self.year}"
        work = f"{base_akn}/2_{self.current_bill if akn_type == 'bill' else self.current_act}"
        date = datetime.now().strftime("%Y-%m-%d")
        postfix = f"/nld@{date};{self.current_bill if akn_type == 'bill' else self.current_act}"
        return FRBR(work=work, expression=work + postfix)

    def as_doel(self):
        if self.doel_id:
            return self.doel_id
        base_format = f"/join/id/proces/{self.province_id}/{self.year}"
        unique_code = uuid4().hex
        # TODO unique code store in DB
        doel_id = f"{base_format}/{self.current_bill}_{unique_code}"
        self.doel_id = doel_id
        return doel_id

    def __str__(self):
        return f"akn_nl_bill_{self.province_id}-2-{self.current_bill}"

    def as_filename(self):
        return self.__str__() + ".xml"

    def as_dict(self):
        return {
            "bill": self.as_FRBR(akn_type="bill"),
            "act": self.as_FRBR(akn_type="act"),
            "akn": self.__str__,
        }
