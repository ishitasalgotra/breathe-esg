# Tradeoffs

1. Emission factor calculation is omitted. The assignment asks for ingestion and normalized review; adding factor libraries without PM signoff risks false precision.

2. Async processing is omitted. Celery/RQ would be appropriate for very large files, but synchronous processing is simpler and defensible for a 4-day MVP.

3. Deep source-specific APIs are omitted. SAP, utility providers, and travel tools vary heavily by customer. CSV import proves the data model and review workflow first.
