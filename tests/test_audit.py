import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from tools.audit_assets import audit, main, validate_inventory, validate_rules


def asset(name="SM_Chair", kind="StaticMesh", path=None):
    return {"path": path or f"/Game/Props/{name}.{name}", "name": name, "class": kind}


class AuditTests(unittest.TestCase):
    def test_valid_prefix_and_unknown_class(self):
        result = audit([asset(), asset("Footstep", "SoundWave")], {"StaticMesh": "SM_"})
        self.assertEqual(result["checked"], 1)
        self.assertEqual(result["issues"], [])
        self.assertEqual(result["skipped_classes"], ["SoundWave"])

    def test_bad_prefix_and_duplicate_path(self):
        item = asset("Chair")
        result = audit([item, dict(item)], {"StaticMesh": "SM_"})
        reasons = [issue["reason"] for issue in result["issues"]]
        self.assertEqual(reasons.count("StaticMesh names should start with SM_"), 2)
        self.assertIn("duplicate inventory path", reasons)

    def test_inventory_validation(self):
        for data in ([], {}, {"assets": [None]}, {"assets": [{"path": ""}]}):
            with self.subTest(data=data), self.assertRaises(ValueError):
                validate_inventory(data)

    def test_rules_validation(self):
        for rules in ([], {}, {"StaticMesh": ""}, {"StaticMesh": 42}):
            with self.subTest(rules=rules), self.assertRaises(ValueError):
                validate_rules(rules)

    def test_cli_exit_codes_and_json(self):
        with tempfile.TemporaryDirectory() as directory:
            inventory = Path(directory) / "inventory.json"
            rules = Path(directory) / "rules.json"
            rules.write_text(json.dumps({"StaticMesh": "SM_"}), encoding="utf-8")
            for name, expected in (("SM_Chair", 0), ("Chair", 1)):
                inventory.write_text(json.dumps({"assets": [asset(name)]}), encoding="utf-8")
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    code = main([str(inventory), "--rules", str(rules), "--json"])
                self.assertEqual(code, expected)
                self.assertEqual(json.loads(output.getvalue())["checked"], 1)
            inventory.write_text("not json", encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(main([str(inventory)]), 2)


if __name__ == "__main__":
    unittest.main()
