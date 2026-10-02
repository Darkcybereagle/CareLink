# Category 1 test guide

## Backend
From backend with the virtual environment active:

    python -m pip install -r requirements-dev.txt
    python -m alembic upgrade head
    pytest -q
    python -m uvicorn app.main:app --reload

The migration must complete, pytest must pass, and the API must start without import errors.

## Mobile
From mobile:

    npm install
    npx expo install --fix
    npm run typecheck

Start separate clients:

    npm run patient

In a second PowerShell:

    npm run provider

Patient uses port 8081 and provider uses 8082. Each command produces its own Expo QR session and the client enforces the matching account role.

## API connectivity
Copy mobile/.env.example to mobile/.env and set EXPO_PUBLIC_API_URL to the PC LAN address.

Optional remote development API:

    cloudflared tunnel --url http://localhost:8000

Set EXPO_PUBLIC_API_URL to the generated HTTPS URL and restart both Expo sessions. Quick Tunnel URLs are temporary development endpoints.

## Data safety
Category 1 does not recreate or wipe the developer PostgreSQL database. Alembic upgrades the existing schema in place. Pytest uses an isolated SQLite database and does not use developer PostgreSQL data.
