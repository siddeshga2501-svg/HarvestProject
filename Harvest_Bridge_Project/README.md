# Harvest Bridge

**SELL BEFORE IT SPOILS** — a full-stack, urgency-first produce marketplace for Hackwarts 2026 (Agritech).

This project combines the concept PDF's **List → Match → Connect** flow with the implementation requirements in the two supplied text files. Farmers publish harvest lots, buyers browse and publish needs, a rule-based matching score explains its reasons, and buyer enquiries are saved in the database. Urgent lots are listed first.

## What's included

- React + Vite responsive interface with English, Kannada and Hindi translations, including crop names, mobile PIN/OTP account screens, map actions, risk indicators, farmer read-aloud controls and an interactive eight-chapter animated guide in English, Kannada and Hindi, with optional browser narration.
- FastAPI REST API with SQLAlchemy, JWT role checks, Argon2 password hashing, filtering, validated image upload, enquiries and OpenAPI docs.
- PostgreSQL configuration and Docker Compose; SQLite is the default local fallback.
- Farmer, buyer and admin roles. Admin accounts are seeded/configured; public registration only accepts farmer and buyer.
- Crop and harvest-date urgency estimates, explicit freshness disclaimer, explainable requirement matching, organic verification state, contact links and admin priority controls.
- Dated mandi record storage and extension points. No fabricated live prices are included.
- Demo data uses fictional names, phone numbers from a reserved demo range and seller-entered prices.
- Backend tests and an Alembic migration baseline.

Official mandi data, Cloudinary, weather and SMS providers require credentials and configured adapters. Until available, the app reports the service as unavailable or uses local image upload. Local development OTP codes are returned by the API for demonstration; never expose that fallback publicly. SMS delivery is intentionally disabled outside development until a provider is integrated. Browser speech is optional and depends on installed browser voices; text entry remains available, and listing publication always requires farmer review.

## Run locally (SQLite)

Requirements: Python 3.11+, Node.js 20+, npm.

1. Copy `.env.example` to `.env`; set a long random `SECRET_KEY` for non-demo use.
2. In a terminal:

   ```powershell
   cd backend
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   python seed.py
   uvicorn app.main:app --reload
   ```

3. In a second terminal:

   ```powershell
   cd frontend
   npm install
   npm run dev
   ```

4. Open http://localhost:5173. API docs are at http://localhost:8000/docs.

The API creates the configured tables on startup. To run explicit migrations use `cd backend; alembic upgrade head`.

## PostgreSQL / Docker Compose

Copy `.env.example` to `.env`, set `SECRET_KEY`, then run `docker compose up --build`. Seed demo records with `docker compose exec backend python seed.py`. The Compose DB password is for local demonstration only; use managed secrets in deployments.

For managed PostgreSQL, set `DATABASE_URL` to `postgresql+psycopg://user:password@host:5432/database` in the backend environment.

## Demo logins

Seed with `python backend/seed.py` after installing dependencies, or run inside the backend container. Accounts and contact numbers are fictional.

| Role | Login | Password |
| --- | --- | --- |
| Farmer | `0000000001` | PIN `2026` |
| Farmer | `0000000002` | PIN `2026` |
| Buyer | `buyer@harvestbridge.demo` | `BuyerDemo!2026` |
| Buyer | `buyer2@harvestbridge.demo` | `BuyerDemo!2026` |
| Admin | `admin@harvestbridge.demo` | `HarvestDemo!2026` |

Set `ADMIN_EMAIL` and `ADMIN_PASSWORD` before seeding to change admin credentials. Never reuse demo passwords publicly.

For farmer signup locally, enter a phone number, choose **Send OTP**, then use the development code displayed by the API response, verify it, and set a four-digit PIN. The development OTP is temporary and held in server memory. SMS delivery needs an SMS provider adapter before production use. Map links search only the village/district/state entered on a listing; the app does not collect or publish precise GPS coordinates. Risk rings are estimates: green 0–30%, yellow 31–60%, orange 61–80%, red 81–100%.

## Checks

Backend tests: `cd backend; pytest`. Frontend production build: `cd frontend; npm run build`. The included tests cover the risk estimator, matching and API health; this project does not claim a full browser end-to-end suite or live-provider integration checks.

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for Vercel, Render and managed PostgreSQL guidance. Configure `VITE_API_URL`, `DATABASE_URL`, `SECRET_KEY`, `FRONTEND_ORIGINS` and provider keys in the deployment dashboards. This workspace does not create a public hosted URL.

## Important limits

- Risk is a configurable planning estimate based on crop shelf-life examples and harvest date. It is not a freshness test or scientific spoilage measurement.
- Match scores use disclosed deterministic rules and actual listing and requirement fields, not AI prediction.
- Mandi records are only as trustworthy as source/date entered by an authorized admin. This build does not claim a live Agmarknet/eNAM connection. Check `/api/health` and `/api/prices`.
- Phone visibility is configurable; precise GPS coordinates are not collected in this release. Map links use only the public locality fields entered for a listing.
- Deal confirmation is recorded as unpaid. No payment is processed.
- Browser speech support and Kannada/Hindi voice availability vary by device and installed voices.
