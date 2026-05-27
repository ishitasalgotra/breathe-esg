# TRADEOFFS.md

# 1. No Enterprise SSO

Not implemented:
- Okta
- Azure AD
- Google Workspace SSO

Reason:
Authentication complexity was deprioritized in favor of ingestion, normalization, and audit workflows.

Production approach:
Enterprise SSO and RBAC would be required.

---

# 2. No Async Ingestion Pipeline

Uploads are processed synchronously.

Reason:
The prototype focused on correctness and traceability rather than ingestion throughput.

Production approach:
Use Celery, Kafka, or background workers.

---

# 3. No PDF Utility Parsing

Utility ingestion only supports CSV uploads.

Reason:
PDF extraction would significantly increase implementation complexity within the 4-day constraint.

Production approach:
OCR + structured extraction pipeline.

---

# 4. No Direct SAP Integration

The prototype uses exported SAP-style files rather than live APIs.

Reason:
Real SAP integrations differ significantly between enterprises.

Production approach:
Support OData/BAPI/IDoc integrations.

---

# 5. Simplified Emission Calculations

The prototype focuses on ingestion and review workflows rather than scientifically accurate carbon accounting.

Reason:
The assignment emphasized normalization and operational handling.

Production approach:
Integrate audited emission factor datasets and methodology engines.
