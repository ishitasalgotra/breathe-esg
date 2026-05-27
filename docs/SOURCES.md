# Source Assumptions

SAP procurement and fuel exports often include plant codes, material identifiers, posting dates, quantities, units, and currency fields. German SAP header variants such as `WERK`, `MENGE`, `EINHEIT`, `WAERS`, and `BUDAT` are accepted.

Utility electricity data is modeled around meter identifiers, billing start/end dates, kWh usage, tariff, and cost. Billing periods can cross month boundaries, so the validator only flags malformed or reversed periods.

Travel data follows common Concur/Navan-style exports: employee, trip type, transport category, airports, nights, and distance. When air distance is missing, the MVP infers great-circle distance for a small airport map.

Limitations: no certified emission factors, no invoice PDF OCR, no vendor API syncing, and a deliberately small airport mapping table.
