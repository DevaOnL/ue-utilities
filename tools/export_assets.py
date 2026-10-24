"""Run inside Unreal Editor's Python console to export an asset inventory."""

import json
from pathlib import Path


def export_assets(root="/Game", destination=None):
    """Export asset metadata without loading or changing the assets themselves."""
    import unreal

    root = root.rstrip("/")
    if root != "/Game" and not root.startswith("/Game/"):
        raise ValueError("root must be /Game or a folder below /Game")
    if destination is None:
        destination = Path(unreal.Paths.project_saved_dir()) / "asset-inventory.json"
    destination = Path(destination).expanduser().resolve()

    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    registry.wait_for_completion()
    assets = []
    for asset in registry.get_assets_by_path(root, recursive=True):
        class_path = asset.asset_class_path
        assets.append({
            "path": f"{asset.package_name}.{asset.asset_name}",
            "name": str(asset.asset_name),
            "class": str(class_path.asset_name),
        })
    inventory = {"root": root, "assets": sorted(assets, key=lambda item: item["path"])}
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    unreal.log(f"Exported {len(assets)} assets to {destination}")
    return destination
