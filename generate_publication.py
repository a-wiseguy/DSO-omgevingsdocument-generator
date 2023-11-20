import glob

from app.build import PublicationService
from app.models import PublicationSettings, DocumentType, AKN
from app.gio.gio_service import GioService
from app.gio.models import Werkingsgebied
from app.policy_objects import PolicyObjects

from utils.helpers import load_json_data

INPUT_FILE_VISIE = "input/publication/omgevingsvisie.json"
INPUT_FILE_PROGRAMMA = "input/publication/omgevingsprogramma.json"


# Example visie
settings = PublicationSettings(
    document_type=DocumentType.VISIE,
    previous_akn_act=44,
    previous_akn_bill=2096,
    publicatie_datum="2023-12-15"
)

new_akn = AKN(
    province_id=settings.provincie_id,
    previous_act=settings.previous_akn_act,
    previous_bill=settings.previous_akn_bill,
)

objects_data = load_json_data("input/policy-objects/mock-data.json")
policy_objects: PolicyObjects = PolicyObjects(objects_data)

service = PublicationService(settings=settings, akn=new_akn, input_file=INPUT_FILE_VISIE)
service.setup_publication_document()

gio_service = GioService(
    act_akn=new_akn.as_FRBR(akn_type="act"),
    publication_settings=settings
)

werkingsgebieden_jsons = glob.glob("./input/werkingsgebieden/*.json")
for werkingsgebieden_json in werkingsgebieden_jsons:
    data = load_json_data(werkingsgebieden_json)
    gio_service.add_werkingsgebied(Werkingsgebied(**data))


service.add_geo_files(gio_service.generate_files(), gio_service.get_refs())
service.build_publication_files(policy_objects)
