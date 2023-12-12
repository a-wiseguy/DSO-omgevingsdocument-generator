import shutil
from typing import List

from app.builder.services import BuilderService
from app.builder.services.lvbb.manifest_builder import ManifestBuilder
from app.builder.services.lvbb.opdracht_builder import OpdrachtBuilder
from app.builder.services.ow.ow_regelingsgebied_builder import OwRegelingsgebiedBuilder
from app.builder.state_manager.models import FileContentData, StrContentData
from app.builder.state_manager.state_manager import StateManager
from app.input_data.input_data_loader import InputData
from app.utils.os import empty_directory


class Builder:
    def __init__(self, input_data: InputData):
        self._state_manager: StateManager = StateManager(input_data)
        self._services: List[BuilderService] = [
            OpdrachtBuilder(),
            OwRegelingsgebiedBuilder(),
            ManifestBuilder(),
        ]

    def build_publication_files(self):
        for service in self._services:
            self._state_manager = service.apply(self._state_manager)

    def save_files(self, output_dir: str):
        empty_directory(output_dir)

        for output_file in self._state_manager.get_output_files():
            destination_path = f"{output_dir}/{output_file.filename}"
            match output_file.content:
                case StrContentData():
                    with open(destination_path, "w") as f:
                        f.write(output_file.content.content)

                case FileContentData():
                    shutil.copy2(output_file.content.source_path, destination_path)
