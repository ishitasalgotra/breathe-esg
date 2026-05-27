from decimal import Decimal
from django.test import SimpleTestCase
from ingestion.utils.normalization import haversine_km, normalize_value, parse_date


class NormalizationTests(SimpleTestCase):
    def test_liters_and_gallons_normalize_to_liters(self):
        value, unit = normalize_value("10", "gal", "liters")
        self.assertEqual(unit, "liters")
        self.assertEqual(value, Decimal("37.8541"))

    def test_messy_dates_are_parsed(self):
        self.assertEqual(str(parse_date("15.02.2026")), "2026-02-15")
        self.assertEqual(str(parse_date("20260131")), "2026-01-31")

    def test_airport_distance_can_be_inferred(self):
        self.assertGreater(haversine_km("JFK", "LHR"), Decimal("5000"))
