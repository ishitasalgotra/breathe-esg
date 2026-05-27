# Engineering Decisions

CSV ingestion was chosen because SAP exports, utility portal downloads, and travel expense tools commonly land with analysts as CSV files. The rejected alternative was direct API integrations; those are better long term but would bury the assignment under vendor-specific credentials.

The ingestion pipeline creates records for suspicious or malformed rows instead of discarding them. That supports analyst review and gives an audit trail of what was wrong.

The service layer is intentionally small: parsers handle CSV shape, normalization utilities handle units/dates/airports, and the pipeline coordinates persistence. This avoids a large framework while preserving testable boundaries.

Questions for a PM: exact emission factor methodology, whether rejected records should be exportable, supported countries/currencies, and whether tenant isolation needs database schemas instead of row-level tenant keys.
