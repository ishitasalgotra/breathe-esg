# DECISIONS.md

# CSV-Based Ingestion

CSV uploads were chosen for the prototype because:
- enterprise exports commonly support CSV
- easier local testing
- lower integration complexity
- realistic for operational analyst workflows

---

# SAP Export Design

SAP flat-file style exports were modeled instead of live SAP APIs.

Reasoning:
- realistic enterprise onboarding often starts with exports
- SAP integrations vary heavily by customer
- localized headers and inconsistent units are common

German-style columns and inconsistent formats were intentionally included.

---

# Utility Data Choice

Utility CSV exports were chosen instead of PDF parsing.

Reasoning:
- PDF extraction would dominate prototype complexity
- many facilities teams already export CSVs from portals
- allowed focus on normalization and validation

---

# Travel Data Design

Travel ingestion was modeled after Concur/Navan-style exports.

Airport codes were used because:
- travel APIs often expose airport metadata rather than calculated distances
- downstream systems typically calculate emissions separately

---

# Suspicious Record Detection

Validation rules were intentionally included because ESG source data quality is inconsistent.

Examples:
- malformed dates
- negative usage
- missing airport codes
- unrealistic quantities

---

# Approval Workflow

Analyst approvals were included because ESG reporting requires human verification before audit signoff.

Approved rows become locked to preserve auditability.

---

# Audit Logging

Immutable audit history was prioritized to support:
- traceability
- compliance workflows
- reviewer accountability

---

# Role Separation

Analyst and Auditor roles were separated to model governance boundaries.

Analysts:
- operational review

Auditors:
- read-only verification

---

# Technology Choices

## Django REST Framework
Chosen for:
- rapid API development
- ORM support
- authentication tooling
- PostgreSQL compatibility

## React
Chosen for:
- fast dashboard iteration
- reusable UI components
- strong ecosystem

## PostgreSQL
Chosen for:
- relational consistency
- audit-safe persistence
- production readiness

---

# PM Questions

If more time were available, key product questions would include:
- expected ingestion volume
- required emission factor methodology
- tenant isolation guarantees
- expected approval SLAs
- expected ERP integrations
- utility PDF requirements