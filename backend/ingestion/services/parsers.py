import csv
from io import TextIOWrapper

HEADER_ALIASES = {"plant code": "plant_code", "werk": "plant_code", "werks": "plant_code", "material": "material", "fuel type": "fuel_type", "kraftstoff": "fuel_type", "quantity": "quantity", "menge": "quantity", "unit": "unit", "einheit": "unit", "currency": "currency", "waers": "currency", "date": "date", "budat": "date", "meter id": "meter_id", "billing start": "billing_start", "billing end": "billing_end", "kwh": "kwh", "tariff": "tariff", "cost": "cost", "employee id": "employee_id", "trip type": "trip_type", "departure airport": "departure_airport", "arrival airport": "arrival_airport", "hotel nights": "hotel_nights", "distance": "distance", "transport category": "transport_category"}


def canonical_header(header):
    return HEADER_ALIASES.get((header or "").strip().lower(), (header or "").strip().lower().replace(" ", "_"))


def parse_csv(file_obj):
    file_obj.seek(0)
    wrapper = TextIOWrapper(file_obj, encoding="utf-8-sig", newline="")
    sample = wrapper.read(2048)
    wrapper.seek(0)
    dialect = csv.Sniffer().sniff(sample, delimiters=",;\t") if sample else csv.excel
    reader = csv.DictReader(wrapper, dialect=dialect)
    reader.fieldnames = [canonical_header(h) for h in (reader.fieldnames or [])]
    for index, row in enumerate(reader, start=2):
        yield index, {canonical_header(k): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
