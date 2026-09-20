# CareLink Architecture

## Core Flow

Mobile/Web clients -> FastAPI -> PostgreSQL / Redis / AI / external services.

Clients never connect directly to PostgreSQL or an LLM provider.

## Applications

- Mobile: React Native + Expo + TypeScript
- Web: Next.js + TypeScript
- API: FastAPI + Python
- Database: PostgreSQL
- Cache/queues: Redis
- Offline local storage: SQLite
- Realtime: WebSockets

## API Modules

- /api/v1/auth
- /api/v1/users
- /api/v1/patients
- /api/v1/providers
- /api/v1/hospitals
- /api/v1/appointments
- /api/v1/home-visits
- /api/v1/ai
- /api/v1/voice
- /api/v1/messages
- /api/v1/notifications
- /api/v1/payments
- /api/v1/medical-records

## Safety

AI supports intake, education, routing and clinician handoff. It must not present itself as a replacement for qualified clinical care. Red-flag safety checks must take priority over ordinary conversational flows.

## Phase 4 implementation

The first AI slice is intentionally deterministic and server-side. It accepts patient-reported symptoms, checks configured safety signals, creates a structured intake summary and returns a care-routing step. It does not diagnose or prescribe.

A later AI provider can be connected behind this same API boundary without changing the mobile client contract.
