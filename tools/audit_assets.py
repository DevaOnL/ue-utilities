#!/usr/bin/env python3
"""Check asset prefixes in an exported inventory; never modifies assets."""

import argparse
import json
import sys
from pathlib import Path


DEFAULT_RULES = Path(__file__).resolve().parents[1] / "config" / "prefixes.json"


def validate_inventory(data):
    if not isinstance(data, dict) or not isinstance(data.get("assets"), list):
        raise ValueError("inventory must be an object with an 'assets' list")
    assets = data["assets"]
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            raise ValueError(f"asset {index}: expected an object")
        for field in ("path", "name", "class"):
            if not isinstance(asset.get(field), str) or not asset[field].strip():
                raise ValueError(f"asset {index}: '{field}' must be a nonempty string")
    return assets


def validate_rules(rules):
    if not isinstance(rules, dict) or not rules:
        raise ValueError("prefix rules must be a nonempty object")
    if any(
        not isinstance(kind, str) or not kind.strip()
        or not isinstance(prefix, str) or not prefix.strip()
        for kind, prefix in rules.items()
    ):
        raise ValueError("prefix rules must map nonempty class names to nonempty prefixes")
    return rules


def audit(assets, rules):
    issues = []
    skipped = set()
    checked = 0
    seen = set()
    for asset in sorted(assets, key=lambda item: (item["path"], item["name"])):
        path = asset["path"]
        if path in seen:
            issues.append({"path": path, "reason": "duplicate inventory path"})
        seen.add(path)
        prefix = rules.get(asset["class"])
        if prefix is None:
            skipped.add(asset["class"])
            continue
        checked += 1
        if not asset["name"].startswith(prefix):
            issues.append({
                "path": path,
                "reason": f"{asset['class']} names should start with {prefix}",
            })
    return {
        "total": len(assets),
        "checked": checked,
        "skipped_classes": sorted(skipped),
        "issues": issues,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inventory", type=Path, help="JSON asset inventory")
    parser.add_argument("--rules", type=Path, default=DEFAULT_RULES)
    parser.add_argument("--json", action="store_true", help="print a JSON report")
    args = parser.parse_args(argv)
    try:
        data = json.loads(args.inventory.read_text(encoding="utf-8"))
        rules = validate_rules(json.loads(args.rules.read_text(encoding="utf-8")))
        result = audit(validate_inventory(data), rules)
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Checked {result['checked']} of {result['total']} assets.")
        for issue in result["issues"]:
            print(f"{issue['path']}: {issue['reason']}")
        if result["skipped_classes"]:
            print("No rule for: " + ", ".join(result["skipped_classes"]))
        print(f"{len(result['issues'])} issue(s).")
    return 1 if result["issues"] else 0


if __name__ == "__main__":
    sys.exit(main())
