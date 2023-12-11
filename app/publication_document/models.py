from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel

from app.input_data.resource.policy_object.policy_object_repository import PolicyObjects
from app.models import AKN, Besluit, ProcedureVerloop, PublicatieOpdracht, Regeling
from app.publication_document.visie import generate_regeling_vrijetekst_lichaam_visie


class PublicationDocument(BaseModel):
    template: Optional[str]
    input_data: Optional[str]
    bill: Optional[Besluit]
    act: Optional[Regeling]
    procedure: Optional[ProcedureVerloop]

    @abstractmethod
    def generate_regeling_vrijetekst_lichaam(self, objects: PolicyObjects):
        pass


class OmgevingsVisie(PublicationDocument):
    template: Optional[str] = "templates/omgevingsvisie/child_of_RegelingVrijetekst.xml"
    input_data: Optional[str] = "input/publication/omgevingsvisie.json"

    def generate_regeling_vrijetekst_lichaam(self, objects: PolicyObjects):
        return generate_regeling_vrijetekst_lichaam_visie(objects)


class OmgevingsProgramma(PublicationDocument):
    template: Optional[str] = "templates/omgevingsprogramma/child_of_RegelingVrijetekst.xml"
    input_data: Optional[str] = "input/publication/omgevingsprogramma.json"

    def generate_regeling_vrijetekst_lichaam(self, objects: PolicyObjects):
        raise NotImplementedError()


class LVBBPublication(BaseModel):
    akn: Optional[AKN]
    opdracht: Optional[PublicatieOpdracht]
    document: Optional[PublicationDocument]
