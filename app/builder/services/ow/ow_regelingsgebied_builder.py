from app.builder.services import BuilderService
from app.builder.state_manager.models import OutputFile, StrContentData
from app.builder.state_manager.state_manager import StateManager
from app.models import ContentType, PublicatieOpdracht
from app.services.utils.helpers import load_template


class OwRegelingsgebiedBuilder(BuilderService):
    def apply(self, state_manager: StateManager) -> StateManager:
        opdracht_file = self._create_opdracht_file(
            state_manager.input_data.publication_settings.opdracht,
        )
        state_manager.add_output_file(opdracht_file)

        return state_manager

    def _create_opdracht_file(self, opdracht: PublicatieOpdracht) -> OutputFile:
        content = load_template(
            "templates/ow/owRegelingsgebied.xml",
            pretty_print=True,
            opdracht=opdracht,
        )
        output_file = OutputFile(
            filename="owRegelingsgebied.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
