from app.input_data.resource.asset.asset_repository import AssetRepository
from app.input_data.resource.policy_object.policy_object_resource_loader import PolicyObjectResourceLoader
from app.input_data.resource.werkingsgebied.werkingsgebied_repository import WerkingsgebiedRepository

from .resources import Resources


class ResourceLoader:
    def __init__(self, resources_config: dict, base_dir: str):
        self._resources_config: dict = resources_config
        self._base_dir: str = base_dir

    def load(self) -> Resources:
        policy_object_loader = PolicyObjectResourceLoader(
            self._base_dir,
            self._resources_config.get("policy-objects", []),
        )
        policy_object_repository = policy_object_loader.load()

        resources = Resources(
            policy_object_repository=policy_object_repository,
            asset_repository=AssetRepository(),
            werkingsgebied_repository=WerkingsgebiedRepository(),
        )
        return resources
