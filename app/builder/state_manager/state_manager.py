from typing import List

from app.builder.state_manager.models import OutputFile
from app.input_data.input_data_loader import InputData


class StateManager:
    def __init__(self, input_data: InputData):
        self.input_data: InputData = input_data
        self._output_files: List[OutputFile] = []

    def add_output_file(self, output_file: OutputFile):
        self._output_files.append(output_file)
