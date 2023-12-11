import os
from dataclasses import dataclass
from typing import List

from app.input_data.besluit import Besluit
from app.input_data.regeling import Regeling
from app.input_data.resource.resource_loader import ResourceLoader
from app.input_data.resource.resources import Resources
from app.models import ProcedureStap, ProcedureVerloop, PublicationSettings
from app.utils.helpers import load_json_data


@dataclass
class InputData:
    publication_settings: PublicationSettings
    besluit: Besluit
    regeling: Regeling
    procedure_verloop: ProcedureVerloop
    resources: Resources


class InputDataLoader:
    def __init__(self, main_file_path: str):
        self._main_file_path: str = main_file_path
        self._base_dir: str = os.path.dirname(main_file_path)

    def load(self) -> InputData:
        main_config: dict = load_json_data(self._main_file_path)

        publication_settings = PublicationSettings.from_json(main_config["settings"])

        besluit = self._create_besluit(main_config["besluit"])

        regeling = self._create_regeling(main_config["regeling"])

        procedure_verloop = self._create_procedure_verloop(
            publication_settings,
            main_config["procedure"],
        )

        resource_loader = ResourceLoader(
            main_config["resources"],
            self._base_dir,
        )
        resources: Resources = resource_loader.load()

        data = InputData(
            publication_settings=publication_settings,
            besluit=besluit,
            regeling=regeling,
            procedure_verloop=procedure_verloop,
            resources=resources,
        )
        return data

    def _create_besluit(self, besluit_config: dict):
        besluit = Besluit.model_validate(besluit_config)
        return besluit

    def _create_regeling(self, besluit_config: dict):
        besluit = Regeling.model_validate(besluit_config)
        return besluit

    def _create_procedure_verloop(
        self,
        publication_settings: PublicationSettings,
        procedure_config: dict,
    ) -> ProcedureVerloop:
        stappen: List[ProcedureStap] = [ProcedureStap.model_validate(s) for s in procedure_config["stappen"]]
        procedure_verloop = ProcedureVerloop(
            bekend_op=publication_settings.datum_bekendmaking,
            stappen=stappen,
        )
        return procedure_verloop
