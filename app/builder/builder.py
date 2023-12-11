from typing import List

from app.builder.services import BuilderService
from app.builder.services.opdracht_builder import OpdrachtBuilder
from app.builder.state_manager.state_manager import StateManager
from app.input_data.input_data_loader import InputData


class Builder:
    def __init__(self, input_data: InputData):
        self._state_manager: StateManager = StateManager(input_data)
        self._services: List[BuilderService] = [
            OpdrachtBuilder(),
        ]

    def build_publication_files(self):
        for service in self._services:
            self._state_manager = service.apply(self._state_manager)
