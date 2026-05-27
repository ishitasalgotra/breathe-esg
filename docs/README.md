# Breathe ESG Assignment

Production-minded MVP for ESG data ingestion and analyst review using Django REST, PostgreSQL, React, Vite, and TailwindCSS.

## Local Setup

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Frontend:

```bash
cd frontend
npm install
copy .env.example .env.local
npm run dev
```

Demo login: `analyst@example.com` / `password123`.

## Environment Variables

Backend uses `DATABASE_URL` on Railway or the individual `POSTGRES_*` variables locally. Configure `SECRET_KEY`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`, and `CSRF_TRUSTED_ORIGINS` for production.

## APIs

- `POST /api/auth/login/`
- `POST /api/ingestion/uploads/`
- `GET /api/ingestion/uploads/status/`
- `GET /api/emissions/records/`
- `GET /api/emissions/records/suspicious/`
- `GET /api/emissions/records/dashboard/`
- `GET /api/approvals/queue/`
- `POST /api/approvals/records/{id}/decision/`
- `GET /api/audit/`

## Railway Deployment

Create a Railway PostgreSQL database, deploy the `backend` directory with the included Dockerfile, set environment variables, and run `python manage.py seed_demo` once from a Railway shell if demo data is desired. Deploy the frontend separately as a Vite static app and set `VITE_API_BASE_URL` to the backend `/api` URL.
