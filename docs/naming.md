# Naming rules

The rules in `config/prefixes.json` are a starting point. They aren't an attempt
to enforce every Unreal convention.

| Class | Prefix | Example |
| --- | --- | --- |
| Blueprint | `BP_` | `BP_DeskLamp` |
| Material | `M_` | `M_Desk` |
| MaterialInstanceConstant | `MI_` | `MI_Desk_Worn` |
| SkeletalMesh | `SK_` | `SK_Mannequin` |
| StaticMesh | `SM_` | `SM_Desk` |
| Texture2D | `T_` | `T_Desk_BaseColor` |
| World | `LV_` | `LV_PaperLantern` |

The checker compares the prefix with the asset name. It doesn't inspect object
contents or infer texture channels. It also doesn't suggest renames: changing
an asset name can affect references and redirectors, which belongs in the editor.

## Custom rules

Copy the JSON file and pass it explicitly:

```sh
python tools/audit_assets.py examples/asset-inventory.json --rules config/prefixes.json
```

Class names are case-sensitive. An unknown class is reported as skipped and
doesn't fail the audit. Add a rule if that class matters to your project.

## Inventory shape

```json
{
  "root": "/Game/Props",
  "assets": [
    {
      "path": "/Game/Props/SM_Desk.SM_Desk",
      "name": "SM_Desk",
      "class": "StaticMesh"
    }
  ]
}
```

Only `assets` and the three fields on each asset are required by the audit.
Extra inventory metadata, such as the sample's workspace label, is ignored.
Duplicate object paths are reported even when both names have valid prefixes.
