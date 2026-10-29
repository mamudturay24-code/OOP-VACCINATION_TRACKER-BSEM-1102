"""Unit tests - run with:  python -m unittest discover -s tests -v"""

import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vaccine_tracker import (Recipient, TrackerError, Vaccine,  # noqa: E402
                             VaccinationTracker, add_record, display_records)

TODAY = date(2026, 10, 6)


class VaccineTests(unittest.TestCase):
    def test_from_schedule_class_method(self):
        v = Vaccine.from_schedule("Pentavalent")
        self.assertEqual((v.doses_required, v.interval_days), (3, 28))

    def test_unknown_vaccine_rejected(self):
        with self.assertRaises(ValueError):
            Vaccine.from_schedule("Unknown")

    def test_static_name_check(self):
        self.assertTrue(Vaccine.is_valid_name("BCG"))
        self.assertFalse(Vaccine.is_valid_name("X"))
        self.assertFalse(Vaccine.is_valid_name("Bad<>name"))

    def test_next_dose_date_instance_method(self):
        v = Vaccine("Test", 2, 10)
        self.assertEqual(v.next_dose_date((date(2026, 1, 1),)), date(2026, 1, 11))
        self.assertIsNone(v.next_dose_date((date(2026, 1, 1), date(2026, 2, 1))))


class RecipientTests(unittest.TestCase):
    def setUp(self):
        Recipient._counter = 0

    def test_create_makes_anonymous_codes(self):
        self.assertEqual(Recipient.create(2025).recipient_id, "VT-0001")
        self.assertEqual(Recipient.create(2024).recipient_id, "VT-0002")
        self.assertEqual(Recipient.total_created(), 2)

    def test_failed_create_is_not_counted(self):
        with self.assertRaises(ValueError):
            Recipient.create(1800)
        self.assertEqual(Recipient.total_created(), 0)

    def test_static_birth_year(self):
        self.assertTrue(Recipient.is_valid_birth_year(2000, 2026))
        self.assertFalse(Recipient.is_valid_birth_year(2030, 2026))
        self.assertFalse(Recipient.is_valid_birth_year("2000", 2026))

    def test_add_dose_keeps_a_tuple(self):
        r = Recipient.create(2025)
        r.add_dose("BCG", date(2026, 1, 1))
        self.assertIsInstance(r.doses_of("BCG"), tuple)
        self.assertEqual(r.total_doses(), 1)


class TrackerTests(unittest.TestCase):
    def setUp(self):
        Recipient._counter = 0
        self.t = VaccinationTracker.with_default_vaccines()
        self.person = self.t.register_recipient(2025)

    def test_record_and_complete(self):
        self.t.record_dose("VT-0001", "BCG", date(2026, 5, 1), TODAY)
        with self.assertRaises(TrackerError):
            self.t.record_dose("VT-0001", "BCG", date(2026, 6, 1), TODAY)

    def test_too_early_refused(self):
        self.t.record_dose("VT-0001", "Pentavalent", date(2026, 9, 1), TODAY)
        with self.assertRaises(TrackerError):
            self.t.record_dose("VT-0001", "Pentavalent", date(2026, 9, 10), TODAY)

    def test_future_date_refused(self):
        with self.assertRaises(TrackerError):
            self.t.record_dose("VT-0001", "BCG", date(2026, 12, 1), TODAY)

    def test_unknown_person_refused(self):
        with self.assertRaises(TrackerError):
            self.t.record_dose("VT-9999", "BCG", date(2026, 5, 1), TODAY)

    def test_due_report(self):
        self.t.record_dose("VT-0001", "Pentavalent", date(2026, 8, 1), TODAY)
        self.assertIn("DUE NOW", self.t.due_report(TODAY))

    def test_duplicate_id_refused(self):
        with self.assertRaises(ValueError):
            add_record({"A": 1}, "A", 2)

    def test_display_records(self):
        out = io.StringIO()
        with redirect_stdout(out):
            self.t.show_all_recipients()
        self.assertIn("VT-0001", out.getvalue())

    def test_no_personal_data_attributes(self):
        names = tuple(vars(self.person))
        for forbidden in ("name", "phone", "address", "email"):
            self.assertNotIn(forbidden, names)


if __name__ == "__main__":
    unittest.main()
