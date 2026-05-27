from decimal import Decimal
from django.db import transaction
from audit.services import write_audit
from emissions.models import EmissionRecord
from ingestion.models import SourceType, UploadStatus
from ingestion.services.parsers import parse_csv
from ingestion.utils.normalization import clean_decimal, haversine_km, normalize_currency, normalize_value, parse_date


def reasons_for_sap(row, quantity, unit, date):
    reasons = []
    if quantity is None: reasons.append("quantity is missing or malformed")
    elif quantity < 0: reasons.append("fuel quantity is negative")
    elif quantity > Decimal("1000000"): reasons.append("fuel quantity exceeds expected enterprise range")
    if not unit: reasons.append("unit is missing")
    if not date: reasons.append("date is missing or invalid")
    if not row.get("plant_code"): reasons.append("plant code is missing")
    return reasons


def reasons_for_utility(row, usage, start, end):
    reasons = []
    if usage is None: reasons.append("kWh value is missing or malformed")
    elif usage < 0: reasons.append("electricity usage is negative")
    elif usage > Decimal("10000000"): reasons.append("electricity usage is unusually high")
    if not start or not end: reasons.append("billing dates are missing or invalid")
    elif end < start: reasons.append("billing end is before billing start")
    if not row.get("meter_id"): reasons.append("meter id is missing")
    return reasons


def reasons_for_travel(row, distance, origin, destination, hotel_nights):
    reasons = []
    if distance is None: reasons.append("distance missing and could not be inferred from airport codes")
    elif distance < 0: reasons.append("travel distance is negative")
    elif distance > Decimal("25000"): reasons.append("travel distance exceeds plausible single-trip range")
    if hotel_nights is not None and hotel_nights < 0: reasons.append("hotel nights is negative")
    if row.get("transport_category", "").lower() == "air" and (not origin or not destination): reasons.append("air travel row is missing airport codes")
    return reasons


def build_record(upload, row_number, row):
    if upload.source_type == SourceType.SAP:
        raw_value = clean_decimal(row.get("quantity")); raw_unit = row.get("unit", "")
        normalized_value, normalized_unit = normalize_value(raw_value, raw_unit, "liters")
        date = parse_date(row.get("date")); reasons = reasons_for_sap(row, raw_value, raw_unit, date)
        return dict(scope_category="Scope 1", emission_category=row.get("fuel_type") or row.get("material") or "Fuel purchase", raw_value=raw_value, raw_unit=raw_unit, normalized_value=normalized_value, normalized_unit=normalized_unit, suspicious_reasons=reasons, metadata={"plant_code": row.get("plant_code"), "material": row.get("material"), "currency": normalize_currency(row.get("currency")), "date": str(date) if date else None, "raw_row": row})
    if upload.source_type == SourceType.UTILITY:
        raw_value = clean_decimal(row.get("kwh")); normalized_value, normalized_unit = normalize_value(raw_value, "kWh", "MWh")
        start, end = parse_date(row.get("billing_start")), parse_date(row.get("billing_end")); reasons = reasons_for_utility(row, raw_value, start, end)
        return dict(scope_category="Scope 2", emission_category="Purchased electricity", raw_value=raw_value, raw_unit="kWh", normalized_value=normalized_value, normalized_unit=normalized_unit, suspicious_reasons=reasons, metadata={"meter_id": row.get("meter_id"), "billing_start": str(start) if start else None, "billing_end": str(end) if end else None, "tariff": row.get("tariff"), "cost": row.get("cost"), "raw_row": row})
    raw_distance = clean_decimal(row.get("distance")); origin, destination = row.get("departure_airport"), row.get("arrival_airport")
    distance = raw_distance or haversine_km(origin, destination); normalized_value, normalized_unit = normalize_value(distance, "km", "km")
    hotel_nights = clean_decimal(row.get("hotel_nights")); reasons = reasons_for_travel(row, distance, origin, destination, hotel_nights)
    transport = (row.get("transport_category") or row.get("trip_type") or "travel").lower()
    category = "Business travel - air" if "air" in transport else "Business travel - ground" if transport in {"rail", "car", "taxi"} else "Business travel"
    return dict(scope_category="Scope 3", emission_category=category, raw_value=raw_distance, raw_unit="km", normalized_value=normalized_value, normalized_unit=normalized_unit, suspicious_reasons=reasons, metadata={"employee_id": row.get("employee_id"), "trip_type": row.get("trip_type"), "departure_airport": origin, "arrival_airport": destination, "hotel_nights": str(hotel_nights) if hotel_nights is not None else None, "distance_inferred": raw_distance is None and distance is not None, "raw_row": row})


@transaction.atomic
def process_upload(upload, user):
    upload.upload_status = UploadStatus.PROCESSING; upload.save(update_fields=["upload_status", "updated_at"])
    created = suspicious = 0
    try:
        for row_number, row in parse_csv(upload.raw_file_path):
            payload = build_record(upload, row_number, row)
            record = EmissionRecord.objects.create(tenant=upload.tenant, source=upload.data_source, source_row_reference=f"{upload.original_filename}:row:{row_number}", suspicious_flag=bool(payload["suspicious_reasons"]), **payload)
            created += 1; suspicious += 1 if record.suspicious_flag else 0
            write_audit(tenant=upload.tenant, entity_type="EmissionRecord", entity_id=record.id, action="ingested", before_value=None, after_value={"source_row_reference": record.source_row_reference, "suspicious_reasons": record.suspicious_reasons}, changed_by=user)
        upload.row_count = created; upload.error_count = suspicious; upload.summary = {"records_created": created, "suspicious_records": suspicious}; upload.upload_status = UploadStatus.COMPLETED_WITH_WARNINGS if suspicious else UploadStatus.COMPLETED
    except Exception as exc:
        upload.upload_status = UploadStatus.FAILED; upload.summary = {"error": str(exc), "records_created_before_failure": created}; raise
    finally:
        upload.save(update_fields=["upload_status", "row_count", "error_count", "summary", "updated_at"])
    return upload
