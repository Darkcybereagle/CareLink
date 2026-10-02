# CareLink

AI-powered healthcare access and care-coordination platform.

## Category 1 foundation
- FastAPI + PostgreSQL + Alembic
- JWT authentication and role-based access
- existing patient/provider workflows retained
- automated pytest integration tests
- PostgreSQL migration CI and TypeScript CI
- separate patient/provider Expo QR sessions without duplicating the codebase
- health and database-readiness endpoints
- architecture boundaries for nurse, verification, realtime, voice, AI/ML, records, quality and external integrations

## Local quality gate
Backend:

    cd backend
    .\venv\Scripts\Activate.ps1
    python -m pip install -r requirements-dev.txt
    python -m alembic upgrade head
    pytest -q

Mobile:

    cd mobile
    npm install
    npx expo install --fix
    npm run typecheck

Run patient and provider clients separately with npm run patient and npm run provider.

See docs/category-1-testing.md.

## Security
Never commit .env files, credentials, API keys, access tokens, patient data or production data.
