# MODEL.md

## Overview

The platform uses a normalized ESG emissions model that consolidates multiple heterogeneous enterprise data sources into a unified reviewable structure.

The core architectural goal was auditability and analyst review rather than raw ingestion throughput.

---

# Core Models

## Tenant

Represents a client organization.

All ingestion records are tenant-scoped to support future enterprise isolation and reporting boundaries.

Fields:
- id
- name
- created_at

Rationale:
Breathe ESG operates across multiple enterprise clients. Tenant separation is necessary for secure reporting and future scalability.

---

## User

Represents platform users.

Roles:
- Analyst
- Auditor

Analysts:
- upload data
- review suspicious records
- approve/reject rows

Auditors:
- read-only access to finalized records

Rationale:
Segregation of duties is important for ESG auditability and governance workflows.

---

## EmissionRecord

Central normalized ESG record model.

Stores:
- source type
- normalized quantity
- units
- timestamps
- approval state
- suspicious flags
- source metadata

Fields:
- source_type
- category
- quantity
- normalized_unit
- source_reference
- suspicious_reason
- approval_status
- approved_by
- approved_at

Rationale:
A unified model simplifies downstream review, reporting, and audit workflows despite inconsistent upstream formats.

---

## UploadBatch

Tracks ingestion jobs.

Stores:
- uploaded file
- upload timestamp
- source type
- uploading analyst

Rationale:
Provides ingestion traceability and debugging visibility.

---

## AuditLog

Immutable event history.

Tracks:
- uploads
- approvals
- rejections
- edits
- timestamps
- acting user

Rationale:
ESG reporting requires audit-safe traceability for compliance and assurance workflows.

---

# Suspicious Record Handling

Records are flagged for:
- negative quantities
- malformed units
- invalid dates
- missing identifiers
- unrealistic values
- malformed travel metadata

Flagged records require analyst review before approval.

Rationale:
Enterprise ESG data quality is highly inconsistent across source systems.

---

# Approval Lifecycle

1. Record ingested
2. Validation executed
3. Suspicious rows flagged
4. Analyst reviews
5. Approved records locked
6. Audit history updated

Rationale:
Supports auditor confidence and traceability.

---

# Unit Normalization

Different source systems use inconsistent units.

Examples:
- liters
- gallons
- barrels
- kWh
- currency-linked quantities

The prototype stores both:
- original source unit
- normalized unit

Rationale:
Preserving source-of-truth data is important for audits.

---

# Scope 1/2/3 Support

The normalized model supports categorization into:
- Scope 1
- Scope 2
- Scope 3

Examples:
- fuel combustion → Scope 1
- electricity → Scope 2
- travel → Scope 3

---

# Tradeoffs

Due to the 4-day prototype constraint:
- ingestion was synchronous
- PDF parsing was omitted
- SSO integration was omitted
- emission factor calculations were simplified

Priority was placed on:
- realistic ingestion
- normalization
- suspicious detection
- auditability
