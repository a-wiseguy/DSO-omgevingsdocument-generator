import glob
from app import assets
from app.assets.assets_service import AssetsService

from app.build import PublicationService
from app.models import PublicationSettings, DocumentType, AKN
from app.gio.gio_service import GioService
from app.gio.models import Werkingsgebied
from app.policy_objects import PolicyObjects

from utils.helpers import load_template_and_write_file, load_json_data
# from utils.eidwid import generate_ew_ids

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

service = PublicationService(
    settings=settings,
    akn=new_akn,
    input_file=INPUT_FILE_VISIE,
    assets_service=assets_service,
)
service.setup_publication_document()

gio_service = GioService(
    act_akn=new_akn.as_FRBR(akn_type="act"),
    publication_settings=settings
)

werkingsgebieden_jsons = glob.glob("./input/werkingsgebieden/*.json")
werkingsgebieden = []
for werkingsgebieden_json in werkingsgebieden_jsons:
    data = load_json_data(werkingsgebieden_json)
    werkingsgebieden.append(Werkingsgebied(**data))

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
document = publication_service.setup_publication_document()
# document.template = "templates/omgevingsvisie/example_visie_no_ids.xml"
publication_service._document = document
publication_service.add_geo_files(geo_files, geo_refs)
output_file = publication_service.build_publication_files(policy_objects)

# # Write ew ids
# generate_ew_ids(input_file=output_file, output_file="output/new_akn.xml")

# print("Created Files:")
# for file in publication_service._created_files:
#     print("Created Files:")
