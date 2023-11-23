import glob
from app import assets
from app.assets.assets_service import AssetsService
from app.build import PublicationService
from app.models import PublicationSettings, DocumentType, AKN
from app.gio.gio_service import GioService
from app.policy_objects import PolicyObjects
from app.ow.ow_service import OWService

from utils.helpers import load_json_data, load_werkingsgebieden

INPUT_FILE_VISIE = "input/publication/omgevingsvisie.json"
INPUT_FILE_PROGRAMMA = "input/publication/omgevingsprogramma.json"

# Example visie / programma
settings = PublicationSettings(
    document_type=DocumentType.VISIE,
    previous_akn_act=88,
    previous_akn_bill=3020,
    publicatie_datum="2023-12-15",
)

new_akn = AKN(
    province_id=settings.provincie_id,
    previous_act=settings.previous_akn_act,
    previous_bill=settings.previous_akn_bill,
)

objects_data = load_json_data("input/policy-objects/mock-data.json")
policy_objects: PolicyObjects = PolicyObjects(objects_data)

assets_jsons = glob.glob("./input/assets/*.json")
assets_data = [load_json_data(json_file) for json_file in assets_jsons]
assets_service = AssetsService(assets_data)

gio_service = GioService(
    act_akn=new_akn.as_FRBR(akn_type="act"), publication_settings=settings
)

werkingsgebieden = load_werkingsgebieden()

# create GML / GIO files
gio_service = GioService(
    act_akn=new_akn.as_FRBR(akn_type="act"),
    publication_settings=settings,
    werkingsgebieden=werkingsgebieden,
)
geo_files = gio_service.generate_files()
geo_refs = gio_service.get_refs()

# Setup publication document
publication_service = PublicationService(
    settings=settings,
    akn=new_akn,
    input_file=INPUT_FILE_VISIE, 
    assets_service=assets_service,
)
publication_service.setup_publication_document()
publication_service.add_geo_files(geo_files, geo_refs)
opdracht = publication_service.build_publication_files(policy_objects)
ow_service = OWService(id_levering=opdracht.id_levering, akn=new_akn)
ow_service.create_all_ow_files()

print("DONE")
