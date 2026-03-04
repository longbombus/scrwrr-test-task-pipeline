import assets

class ValidationAlert:
    def __init__(self, severity: str, description: str):
        self.severity = severity
        self.description = description

class ValidationRule:
    def __init__(self, matcher: callable, checker: callable):
        self.matcher = matcher
        self.checker = checker

rules : list[ValidationRule] = [
    ValidationRule(
        matcher=lambda asset: isinstance(asset, assets.MeshInfo),
        checker=lambda asset: ValidationAlert("Error", f"VertexCount {asset.vertices} > 10000") if asset.vertices > 10000 else None
    ),
    ValidationRule(
        matcher=lambda asset: isinstance(asset, assets.MeshInfo),
        checker=lambda asset: ValidationAlert("Error", f"TriangleCount {asset.triangles} > 5000") if asset.triangles > 5000 else None
    ),
    ValidationRule(
        matcher=lambda asset: isinstance(asset, assets.MeshInfo),
        checker=lambda asset: ValidationAlert("Warning", f"MaterialsCount {asset.materials} > 3") if asset.materials > 3 else None
    ),
    ValidationRule(
        matcher=lambda asset: isinstance(asset, assets.MeshInfo),
        checker=lambda asset: ValidationAlert("Warning", f"Name `{asset.name}` not starts with `SK_` or `SM_`") if not (asset.name.startswith("SK_") or asset.name.startswith("SM_")) else None
    ),
    ValidationRule(
        matcher=lambda asset: isinstance(asset, assets.TextureInfo),
        checker=lambda asset: ValidationAlert("Error", f"Texture size {asset.width}x{asset.height} is not powers of two") if (asset.width & (asset.width - 1)) != 0 or (asset.height & (asset.height - 1)) != 0 else None
    ),
    ValidationRule(
        matcher=lambda asset: isinstance(asset, assets.TextureInfo),
        checker=lambda asset: ValidationAlert("Error", f"Texture file size {asset.fileSize / (1024.0 * 1024.0):.2f} MB > 2MB") if asset.fileSize > 2 * 1024 * 1024 else None
    ),
    ValidationRule(
        matcher=lambda asset: isinstance(asset, assets.TextureInfo),
        checker=lambda asset: ValidationAlert("Warning", f"Texture aspect {asset.width}:{asset.height} is not 1:1 or 1:2 or 2:1") if asset.width != asset.height and asset.width != 2 * asset.height and 2 * asset.width != asset.height else None
    ),
]

def validate(assets_infos : list[assets.AssetInfo]) -> dict[str, list[(assets.AssetInfo, ValidationAlert)]]:
    alerts: dict[str, list[(assets.AssetInfo, ValidationAlert)]] = {}
    for asset_info in assets_infos:
        for rule in rules:
            if rule.matcher(asset_info):
                result : ValidationAlert = rule.checker(asset_info)
                if result is not None:
                    if result.severity not in alerts:
                        alerts[result.severity] = []
                    alerts[result.severity].append((asset_info, result))
    return alerts