# Model Design

The platform uses tenant-scoped relational tables rather than schema-per-tenant isolation. That keeps the MVP deployable on Railway PostgreSQL while still enforcing isolation through foreign keys and queryset filters.

Core flow: `RawUpload` stores the file and status, `DataSource` describes the enterprise source, and `EmissionRecord` stores both raw and normalized values. `ApprovalWorkflow` records analyst decisions and `AuditLog` captures ingestion and approval mutations.

Normalization keeps original values intact. Conversions are applied into canonical units: electricity to MWh, fuel to liters, and travel to km. `NormalizationRule` stores auditable conversion factors while utility code provides deterministic parsing.

Every user belongs to one tenant and every upload, record, approval, and audit event is tenant filtered. Superusers can see all tenants for admin operations.
