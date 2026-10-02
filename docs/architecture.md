# CareLink Architecture

## Category 1 baseline
CareLink is a modular healthcare platform. Patient and provider experiences share one API and one PostgreSQL source of truth, but run as separate Expo development clients/QR sessions.

## Runtime
Patient app / Provider app / Web -> FastAPI API -> PostgreSQL.

Later categories add stable adapters for Redis, queues/workers, WebSockets, AI/model registry, voice, maps, notifications, payments, licence/facility verification, object storage and external clinical systems. Clients never connect directly to PostgreSQL, external verification systems or an LLM.

## API domains
Implemented now: /auth, /users, /ai, /care, /providers.

Reserved domain boundaries for subsequent categories: /patients, /nurses, /doctors, /hospitals, /verification, /appointments, /home-visits, /availability, /matching, /messages, /notifications, /reviews, /quality, /medical-records, /documents, /consent, /audit, /location, /emergency, /voice, /payments, /integrations.

A reserved boundary is never presented as a live integration until its implementation and tests exist.

## Quality gates
Every backend change must pass Alembic upgrade on PostgreSQL and pytest -q. Every mobile change must pass npm run typecheck. GitHub Actions enforces backend tests, PostgreSQL migrations and TypeScript checking.

## Safety
AI supports intake, education, routing and clinician handoff. Emergency/red-flag rules take priority. Production learning must use consented, de-identified data and an evaluated/approved model lifecycle; live patient conversations do not directly retrain the deployed model.
