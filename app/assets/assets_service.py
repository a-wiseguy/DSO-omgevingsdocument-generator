from enum import Enum
from typing import Dict, List, Optional
import uuid

from pydantic import BaseModel, Field, root_validator, validator



class IllustratieFormaat(str, Enum):
    jpg = "image/jpeg"
    jpeg = "image/jpeg"
    png = "image/png"


class IllustratieUitlijning(str, Enum):
    start = "start"
    end = "end"
    center = "center"


class Meta(BaseModel):
    Ext: str = Field(..., alias="ext")
    Breedte: int = Field(..., alias="width")
    Hoogte: int = Field(..., alias="height")
    Size: int = Field(..., alias="size")
    Formaat: IllustratieFormaat = Field(None)
    Uitlijning: IllustratieUitlijning = Field(IllustratieUitlijning.start)
    Dpi: int = Field(150)

    @root_validator(pre=True)
    def generate_formaat(fields: dict):
        fields["Formaat"] = IllustratieFormaat[fields['ext']]
        return fields


class Asset(BaseModel):
    UUID: uuid.UUID
    Content: str
    Meta: Meta

    def get_filename(self) -> str:
        filename: str = f"img_{self.UUID}.{self.Meta.Ext}"
        return filename


class AssetsService:
    def __init__(self, assets: List[dict]):
        self._assets: Dict[str, Asset] = {
            str(a["UUID"]): Asset.model_validate(a)
            for a in assets
        }
    
    def get_optional(self, idx: uuid.UUID) -> Optional[Asset]:
        asset: Optional[Asset] = self._assets.get(str(idx))
        return asset
    
    def get(self, idx: uuid.UUID) -> Asset:
        asset: Optional[Asset] = self.get_optional(idx)
        if asset is None:
            raise RuntimeError(f"Can not find asset {idx}")
        return asset

    def all(self) -> List[Asset]:
        return list(self._assets.values())
