# CareLink Mobile

React Native + Expo + TypeScript patient application.

## Phase 3 delivered

- CareLink welcome screen
- Patient registration
- Patient login
- Authenticated session storage
- Patient profile onboarding
- Patient home dashboard
- FastAPI connection
- CareLink visual foundation: light blue/white, green primary actions, simple healthcare cards

## Phase 4 delivered

- AI-assisted symptom intake
- Configured safety-signal screening
- Care pathway response
- Clinician handoff summary
- AI safety boundary messaging

## Run locally

From the repository root:

    cd mobile
    npm install
    npx expo install --fix
    npm run typecheck

Create mobile/.env from mobile/.env.example.

For Expo Go on a physical phone, use the computer's LAN IPv4 address, for example:

    EXPO_PUBLIC_API_URL=http://192.168.1.10:8000

The phone and computer must be on the same network.

Start the app:

    npm start

Then scan the Expo QR code with Expo Go.

## Backend

The FastAPI backend must be running before registration, login, onboarding and AI intake can work.

Backend:

    cd backend
    .\venv\Scripts\Activate.ps1
    uvicorn app.main:app --reload

Swagger:

    http://127.0.0.1:8000/docs

## Product boundary

Phase 3 and Phase 4 do not add provider matching, hospitals, appointments, chat, voice/video, payments, pharmacy, laboratory, ambulance or other later-phase modules. Those remain in the existing CareLink roadmap.
