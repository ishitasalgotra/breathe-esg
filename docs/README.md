# Breathe ESG Ingestion & Audit Platform

A Django REST + React prototype built for the Breathe ESG Tech Intern Assignment.

This platform ingests emissions and activity data from multiple enterprise sources, normalizes inconsistent records into a unified ESG model, flags suspicious rows for analyst review, and maintains an auditable approval workflow before records are finalized.

---

## Features

- SAP fuel and procurement ingestion
- Utility electricity ingestion
- Corporate travel ingestion
- Unified normalized emissions model
- Suspicious record detection
- Approval workflow
- Immutable audit history
- Analyst and Auditor roles
- Multi-tenant-ready architecture
- PostgreSQL persistence
- React dashboard with ESG analytics

---

## Architecture

### Frontend
- React
- Vite
- TailwindCSS

### Backend
- Django REST Framework
- PostgreSQL

### Deployment
- Railway (backend + database)
- Vercel/Railway (frontend)

---

## ESG Workflow

1. Analyst uploads source data
2. Records are normalized
3. Validation engine flags suspicious rows
4. Analyst reviews and approves records
5. Approved records are locked
6. Audit trail stores all actions

---

## Source Types

### SAP Fuel & Procurement
Modeled after flat-file SAP exports with:
- inconsistent units
- plant codes
- localized/German headers
- malformed dates

### Utility Electricity Data
Modeled after utility portal CSV exports with:
- billing periods
- meter IDs
- tariff structures
- inconsistent usage values

### Corporate Travel Data
Modeled after travel platform exports:
- airport codes
- travel classes
- hotels
- transport categories

---

## Demo Credentials

### Analyst
Email: analyst@example.com  
Password: password123

### Auditor
Email: auditor@example.com  
Password: password123

---

## Local Setup

### Backend

```bash
cd backend
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Deployment Links

Frontend:
https://YOUR_FRONTEND_URL

Backend:
https://YOUR_BACKEND_URL

---

## Screenshots

- Dashboard
- Upload Center
- Suspicious Records
- Approval Queue
- Audit History

(Add screenshots here)

---

## Future Improvements

- Enterprise SSO integration
- Async ingestion jobs
- PDF utility bill parsing
- Automated emission factor engine
- Advanced RBAC permissions
- Real SAP API integrations
- Warehouse-scale ingestion pipelines