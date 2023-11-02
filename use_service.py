from app.build import PublicationDocument, OmgevingsVisie, OmgevingsProgramma, PublicationService
from app.models import PublicationSettings, DocumentType

from utils.helpers import load_template_and_write_file, load_json_data


# Settings / publication metadata
publication_settings = PublicationSettings(
    document_type=DocumentType.VISIE,
    previous_akn_act=44, 
    previous_akn_bill=2096, 
    publicatie_datum="2023-12-15"
)

service = PublicationService(publication_settings)
service.build_publication_files()