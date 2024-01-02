# import glob
# from app import assets
# from app.assets.assets_service import AssetsService
# from app.build import PublicationService
# from app.models import PublicationSettings, DocumentType, AKN
# from app.ewid.ewid_service import EWIDService
# from app.gio.gio_service import GioService
# from app.policy_objects import PolicyObjects
# from app.ow.ow_service import OWService
# from app.utils.helpers import load_json_data, load_werkingsgebieden, create_zip_from_dir, get_checksum_and_size

# INPUT_FILE_VISIE = "input/publication/omgevingsvisie.json"
# INPUT_FILE_PROGRAMMA = "input/publication/omgevingsprogramma.json"

# # Select mock document type
# input_data_publication = load_json_data(INPUT_FILE_VISIE)

# # Example visie / programma
# settings = PublicationSettings.from_json(input_data_publication["settings"])

# new_akn = AKN(
#     province_id=settings.provincie_id,
#     previous_act=settings.previous_akn_act,
#     previous_bill=settings.previous_akn_bill,
# )

# objects_data = load_json_data("input/policy-objects/mock-data.json")
# policy_objects: PolicyObjects = PolicyObjects(objects_data)

# assets_jsons = glob.glob("./input/assets/*.json")
# assets_data = [load_json_data(json_file) for json_file in assets_jsons]
# assets_service = AssetsService(assets_data)

# gio_service = GioService(
#     act_akn=new_akn.as_FRBR(akn_type="act"), publication_settings=settings
# )

# werkingsgebieden = load_werkingsgebieden()

# # create GML / GIO files
# gio_service = GioService(
#     act_akn=new_akn.as_FRBR(akn_type="act"),
#     publication_settings=settings,
#     werkingsgebieden=werkingsgebieden,
# )
# geo_files = gio_service.generate_files()
# geo_refs = gio_service.get_refs()

# # Init EWID service and prefix
# ewid_service = EWIDService(
#     wid_prefix=f"{settings.provincie_id}_{settings.next_akn_id_bill}"
# )

# # Setup publication document
# publication_service = PublicationService(
#     settings=settings,
#     akn=new_akn,
#     input_data=input_data_publication,
#     assets_service=assets_service,
#     ewid_service=ewid_service,
# )
# publication_service.setup_publication_document()
# publication_service.add_geo_files(geo_files, geo_refs)
# opdracht = publication_service.build_publication_files(policy_objects)
# # OW files
# ow_service = OWService(id_levering=opdracht.id_levering, akn=new_akn)
# ow_service.create_all_ow_files(ewid_service.object_references)

# print("finished creating files")

# # Creating a ZIP file
# source_directory = "output/"
# output_zip_path = f"test-validatie.zip"
# create_zip_from_dir(source_directory, output_zip_path)


# print(f"ZIP result: {output_zip_path}")

# # Calculating checksum and size
# checksum, size = get_checksum_and_size(output_zip_path)
# print(f"Checksum: {checksum}")
# print(f"Size: {size}")
