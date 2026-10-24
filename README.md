# UE Utilities

Small Python helpers for Unreal Engine asset housekeeping. Export an inventory
from the editor, then check naming prefixes without opening the project again.
No pip dependencies.

## What's here

| Script | Purpose |
| --- | --- |
| `tools/export_assets.py` | Export asset names, paths and classes from Unreal Editor |
| `tools/audit_assets.py` | Check an inventory against the prefix rules in `config/` |

The exporter reads the asset registry. The audit reads JSON. Neither renames,
loads or saves assets.

## Try the audit

Python 3.10 or newer:

```sh
python tools/audit_assets.py examples/asset-inventory.json
python tools/audit_assets.py examples/asset-inventory.json --json
```

The sample has deliberate naming mistakes. Exit status is `0` for a clean
inventory, `1` for findings, and `2` for invalid input or a file error. Asset
classes without a prefix rule are listed as skipped.

## Export from the editor

The exporter targets Unreal Engine 5.1+ and requires the **Python Editor Script
Plugin**. Enable it and restart the editor. Open the Output Log, select Python,
and add your checkout to the module path:

```python
import sys
sys.path.insert(0, "/absolute/path/to/ue-utilities")
from tools.export_assets import export_assets
export_assets("/Game/Props")
```

The inventory is written to `Saved/asset-inventory.json` in your Unreal project.
Pass `destination="/path/to/inventory.json"` to choose a different location.
It includes assets visible to the editor's registry, including unsaved changes;
save your project first if you need a snapshot of what's on disk.

## Development

```sh
python -m unittest discover -s tests -v
```

The tests exercise the offline audit. The editor exporter requires Unreal and
isn't covered by these tests.

MIT licensed. Small scope: prefix checks, not an asset validator.
