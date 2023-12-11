from dataclasses import dataclass

from app.input_data.resource.asset.asset_repository import AssetRepository
from app.input_data.resource.policy_object.policy_object_repository import PolicyObjectRepository
from app.input_data.resource.werkingsgebied.werkingsgebied_repository import WerkingsgebiedRepository


@dataclass
class Resources:
    policy_object_repository: PolicyObjectRepository
    asset_repository: AssetRepository
    werkingsgebied_repository: WerkingsgebiedRepository
