# SOURCES.md

# 1. SAP Fuel & Procurement Data

## Research

Reviewed:
- SAP flat-file exports
- IDoc concepts
- SAP OData examples
- ERP export patterns

Observed characteristics:
- inconsistent units
- localized headers
- plant codes
- malformed date formats
- operational abbreviations

---

## Prototype Modeling

The prototype intentionally includes:
- German column names
- inconsistent units
- missing identifiers
- malformed dates
- unrealistic quantities

Reason:
Real enterprise ERP exports are rarely clean.

---

## What Would Break In Production

- inconsistent schemas between clients
- custom SAP mappings
- missing master data
- multilingual ERP deployments

---

# 2. Utility Electricity Data

## Research

Reviewed:
- utility portal exports
- energy billing structures
- meter-based reporting

Observed characteristics:
- billing periods
- tariff structures
- irregular reporting cycles
- inconsistent meter metadata

---

## Prototype Modeling

Included:
- missing meter IDs
- overlapping billing periods
- malformed usage values
- inconsistent tariff naming

Reason:
Facilities data is operationally messy.

---

## What Would Break In Production

- utility-specific schemas
- timezone normalization
- interval-based metering
- partial billing periods

---

# 3. Corporate Travel Data

## Research

Reviewed:
- Concur documentation
- Navan platform exports
- expense reporting structures

Observed characteristics:
- airport codes instead of distances
- mixed transport modes
- inconsistent expense metadata
- incomplete trip details

---

## Prototype Modeling

Included:
- airport-only routes
- missing airport codes
- invalid routes
- malformed expense values
- negative hotel nights

Reason:
Travel platforms prioritize expense workflows rather than emissions accuracy.

---

## What Would Break In Production

- duplicate expense claims
- missing itinerary data
- international currency normalization
- partial trip segmentation
```