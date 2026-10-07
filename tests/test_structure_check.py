"""Tests for the dataset structure-check starter script."""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.preprocessing.structure_check import annotation_issues, report, scan


class StructureCheckTests(unittest.TestCase):
    def test_scan_finds_files_in_nested_folders(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "images" / "raw").mkdir(parents=True)
            (root / "metadata").mkdir(parents=True)
            (root / "images" / "raw" / "a.jpg").touch()
            (root / "metadata" / "index.json").touch()

            found = scan(root)
            self.assertEqual(len(found["images/raw"]), 1)
            self.assertEqual(len(found["images/processed"]), 0)
            self.assertEqual(len(found["metadata"]), 1)

    def test_valid_annotation_has_no_issues(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ok.json"
            path.write_text(
                json.dumps({"receipt_id": "x", "merchant": "Store", "date": "2026-10-08", "total": 1.0}),
                encoding="utf-8",
            )
            self.assertEqual(annotation_issues(path), [])

    def test_missing_field_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "partial.json"
            path.write_text(json.dumps({"merchant": "Store", "total": 1.0}), encoding="utf-8")
            self.assertIn("missing field: date", annotation_issues(path))
            self.assertIn("missing field: receipt_id", annotation_issues(path))

    def test_invalid_json_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text("not json at all", encoding="utf-8")
            self.assertTrue(any("not valid JSON" in issue for issue in annotation_issues(path)))

    def test_report_includes_totals(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for rel in ("annotations/raw", "images/raw"):
                (root / rel).mkdir(parents=True)
            (root / "annotations" / "raw" / "ok.json").write_text(
                json.dumps({"receipt_id": "x", "merchant": "Store", "date": "2026-10-08", "total": 5.0}),
                encoding="utf-8",
            )
            text = report(scan(root))
            self.assertIn("TOTAL", text)
            self.assertIn("Annotations checked : 1", text)
            self.assertIn("No problems found", text)


if __name__ == "__main__":
    unittest.main()