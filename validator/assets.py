from dataclasses import dataclass
from typing import Any, Dict, List

@dataclass
class AssetInfo:
    type: str
    name: str

@dataclass
class MeshInfo(AssetInfo):
    vertices: int
    triangles: int
    materials: int

@dataclass
class TextureInfo(AssetInfo):
    width: int
    height: int
    fileSize: int

ASSET_FACTORY = {
    "mesh": MeshInfo,
    "texture": TextureInfo,
}

def parse_assets(payload: Dict[str, Any]) -> List[AssetInfo]:
    assets: List[AssetInfo] = []
    for item in payload.get("assets", []):
        asset_type = item.get("type")
        cls = ASSET_FACTORY.get(asset_type)
        if not cls:
            raise ValueError(f"Unknown asset type: {asset_type}")
        assets.append(cls(**item))
    return assets
