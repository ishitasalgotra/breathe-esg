from datetime import datetime
from decimal import Decimal, InvalidOperation

UNIT_ALIASES = {"kwh": "kWh", "kw h": "kWh", "kilowatt hour": "kWh", "mwh": "MWh", "l": "liters", "liter": "liters", "litre": "liters", "liters": "liters", "ltr": "liters", "gal": "gallons", "gallon": "gallons", "gallons": "gallons", "us gal": "gallons", "km": "km", "kilometer": "km", "kilometers": "km", "mi": "miles", "mile": "miles", "miles": "miles"}
CONVERSIONS = {("kWh", "MWh"): Decimal("0.001"), ("MWh", "kWh"): Decimal("1000"), ("liters", "gallons"): Decimal("0.264172"), ("gallons", "liters"): Decimal("3.78541"), ("miles", "km"): Decimal("1.60934"), ("km", "miles"): Decimal("0.621371")}
DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d.%m.%Y", "%Y%m%d", "%d-%b-%Y", "%d %b %Y"]
AIRPORTS = {"JFK": (40.6413, -73.7781), "LHR": (51.47, -0.4543), "SFO": (37.6213, -122.3790), "BLR": (13.1986, 77.7066), "DEL": (28.5562, 77.10), "FRA": (50.0379, 8.5622), "SIN": (1.3644, 103.9915), "BOM": (19.0896, 72.8656), "DXB": (25.2532, 55.3657)}


def clean_decimal(value):
    if value is None or str(value).strip() == "":
        return None
    try:
        return Decimal(str(value).replace(",", "").strip())
    except InvalidOperation:
        return None


def canonical_unit(unit):
    if not unit:
        return ""
    return UNIT_ALIASES.get(str(unit).strip().lower(), str(unit).strip())


def normalize_value(value, source_unit, target_unit):
    number = clean_decimal(value)
    source = canonical_unit(source_unit)
    target = canonical_unit(target_unit)
    if number is None:
        return None, source
    if source == target:
        return number, target
    factor = CONVERSIONS.get((source, target))
    if factor is None:
        return number, source
    return (number * factor).quantize(Decimal("0.0001")), target


def parse_date(value):
    if not value or not str(value).strip():
        return None
    text = str(value).strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    return None


def normalize_currency(value):
    return str(value).strip().upper() if value is not None else None


def haversine_km(origin, destination):
    from math import asin, cos, radians, sin, sqrt
    a = AIRPORTS.get((origin or "").upper())
    b = AIRPORTS.get((destination or "").upper())
    if not a or not b:
        return None
    lat1, lon1 = map(radians, a)
    lat2, lon2 = map(radians, b)
    dlat, dlon = lat2 - lat1, lon2 - lon1
    h = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return Decimal(str(2 * 6371 * asin(sqrt(h)))).quantize(Decimal("0.1"))
