"""Tests for the receipt label suggester (src/extraction/suggest_labels.py).

These only test local helpers - no API calls, no network.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.extraction.suggest_labels import (
    _currency,
    _iso_date,
    _number,
    clean_record,
    parse_model_json,
    receipt_id_from,
)


class ParseModelJsonTests(unittest.TestCase):
    def test_strips_code_fences(self):
        raw = '```json\n{"merchant": "Store", "total": 12.5}\n```'
        self.assertEqual(parse_model_json(raw), {"merchant": "Store", "total": 12.5})

    def test_extracts_object_from_noisy_text(self):
        raw = 'Sure! Here you go:\n{"merchant": "Cafe", "total": 9.0}\nHope that helps.'
        self.assertEqual(parse_model_json(raw), {"merchant": "Cafe", "total": 9.0})

    def test_unwraps_single_element_array(self):
        raw = '[{"merchant": "Shop", "total": 3.0}]'
        self.assertEqual(parse_model_json(raw), {"merchant": "Shop", "total": 3.0})

    def test_non_object_raises(self):
        with self.assertRaises(ValueError):
            parse_model_json("no json at all here")

    def test_empty_array_raises(self):
        with self.assertRaises(ValueError):
            parse_model_json("[]")


class CleanRecordTests(unittest.TestCase):
    def test_valid_record_is_normalized(self):
        record = clean_record({
            "merchant": "  HELLO MITHILA TOURS & TRAVELS  ",
            "date": "2026-10-05",
            "currency": "npr",
            "subtotal": "1,150.00",
            "tax": 57.5,
            "total": 1207.5,
            "receipt_number": "TKT-MUUSIGVMQO5",
            "receipt_type": "travel",
            "language": "en",
            "items": [
                {"description": "Air ticket", "quantity": 1, "unit_price": 1150, "amount": 1150}
            ],
        })
        self.assertEqual(record["merchant"], "HELLO MITHILA TOURS & TRAVELS")
        self.assertEqual(record["date"], "2026-10-05")
        self.assertEqual(record["currency"], "NPR")
        self.assertEqual(record["subtotal"], 1150.0)
        self.assertEqual(record["tax"], 57.5)
        self.assertEqual(record["total"], 1207.5)
        self.assertEqual(record["receipt_number"], "TKT-MUUSIGVMQO5")
        self.assertEqual(record["items"][0]["amount"], 1150.0)

    def test_empty_strings_become_none(self):
        record = clean_record({
            "merchant": "",
            "date": "",
            "currency": "",
            "subtotal": "",
            "items": [],
        })
        self.assertIsNone(record["merchant"])
        self.assertIsNone(record["date"])
        self.assertIsNone(record["currency"])
        self.assertIsNone(record["subtotal"])
        self.assertEqual(record["items"], [])

    def test_bad_date_become_none(self):
        record = clean_record({"date": "Oct 05, 2026"})
        self.assertIsNone(record["date"])

    def test_malformed_items_become_empty(self):
        record = clean_record({"items": "not a list"})
        self.assertEqual(record["items"], [])

    def test_bad_items_are_dropped(self):
        record = clean_record({"items": [{"description": "ok"}, "junk", 42]})
        self.assertEqual(len(record["items"]), 1)
        self.assertEqual(record["items"][0]["description"], "ok")
        self.assertIsNone(record["items"][0]["quantity"])


class HelperTests(unittest.TestCase):
    def test_number_handles_strings_and_commas(self):
        self.assertEqual(_number("1,207.50"), 1207.5)
        self.assertEqual(_number(57), 57.0)
        self.assertIsNone(_number("abc"))
        self.assertIsNone(_number(None))

    def test_number_rejects_nan_and_infinity(self):
        self.assertIsNone(_number("NaN"))
        self.assertIsNone(_number("inf"))

    def test_iso_date_accepts_only_iso(self):
        self.assertEqual(_iso_date("2026-10-05"), "2026-10-05")
        self.assertIsNone(_iso_date("05/10/2026"))

    def test_currency_accepts_three_letters(self):
        self.assertEqual(_currency("npr"), "NPR")
        self.assertIsNone(_currency("rs"))

    def test_receipt_id_is_a_clean_slug(self):
        self.assertEqual(receipt_id_from(Path("Invoice - TKT-MUUSIGVMQO5.pdf")),
                         "invoice-tkt-muusigvmqo5")


if __name__ == "__main__":
    unittest.main()