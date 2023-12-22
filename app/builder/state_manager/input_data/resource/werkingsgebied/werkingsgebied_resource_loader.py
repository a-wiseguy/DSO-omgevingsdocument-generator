from typing import List

from app.builder.state_manager.input_data.resource.werkingsgebied.werkingsgebied_repository import (
    WerkingsgebiedRepository,
)
from app.models import PublicationSettings
from app.services.utils.helpers import load_json_data
from app.services.utils.os import create_normalized_path


class WerkingsgebiedResourceLoader:
    def __init__(self, base_dir: str, publication_settings: PublicationSettings, werkingsgebied_files: List[str]):
        self._base_dir: str = base_dir
        self._publication_settings: PublicationSettings = publication_settings
        self._werkingsgebied_files: List[str] = werkingsgebied_files

    def load(self) -> WerkingsgebiedRepository:
        repository = WerkingsgebiedRepository(
            self._publication_settings.provincie_id,
            self._publication_settings.expression_taal,
        )

        for werkingsgebied_file in self._werkingsgebied_files:
            path = create_normalized_path(self._base_dir, werkingsgebied_file)
            werkingsgebied = load_json_data(path)
            if isinstance(werkingsgebied, dict):
                repository.add(werkingsgebied)
            else:
                repository.add_list(werkingsgebied)

        return repository
