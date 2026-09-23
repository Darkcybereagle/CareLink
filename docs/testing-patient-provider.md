# CareLink Phase Testing — Patient + Provider

This is the verification checklist for the patient and provider phases added after the existing Phase 3/4 work.

## Patient Phase 5 — Care discovery

1. Login as a patient.
2. Open Find a doctor or hospital.
3. Search by city.
4. Confirm provider cards show provider type, specialty, facility, city and verification state.
5. Confirm hospital cards show facility, address, city and services.
6. Confirm no provider can be booked unless verified.

## Local provider verification test

The admin verification workflow is intentionally deferred. For local end-to-end testing only, after creating a provider profile you may mark that test provider verified directly in PostgreSQL:

    UPDATE provider_profiles SET verification_status = 'VERIFIED' WHERE user_id = YOUR_PROVIDER_USER_ID;

Do not use this as the production verification workflow. The future admin phase will own provider verification.

## Patient Phase 6 — Appointments and home care

1. Use a verified provider.
2. Request an appointment with a future date/time and reason.
3. Confirm the appointment appears under Appointments.
4. Login as the provider and confirm the request appears in provider appointments.
5. Confirm the provider can move requested -> confirmed -> completed.
6. Return to patient and confirm the status notification exists.
7. Request home care with address and reason.
8. Confirm the request appears in patient care activity.
9. Provider accepts the home visit and later marks it completed.
10. Confirm the patient receives status notifications.

## Patient Phase 7 — Secure communication and follow-up

1. Open a provider from the directory.
2. Start a message thread.
3. Send a patient message.
4. Confirm the provider can see the thread and reply.
5. Confirm the patient receives a notification for the provider reply.
6. Create a follow-up request with a provider and future date/time.
7. Confirm it appears in patient activity and provider follow-ups.

## Provider Phase 1 — Professional onboarding

1. Start a fresh CareLink account.
2. Choose Doctor or Nurse during registration.
3. Complete professional profile.
4. Confirm the profile starts as pending verification.
5. Confirm provider accounts do not enter the patient onboarding flow.

## Provider Phase 2 — Availability, appointments and home care

1. Add weekly availability.
2. Confirm the availability appears in the provider profile screen.
3. Use a verified provider to receive a patient appointment request.
4. Confirm the appointment.
5. Mark the appointment completed.
6. Receive a home-care request.
7. Accept it.
8. Mark it completed.

## Provider Phase 3 — Clinical handoff and communication

1. Have a patient submit an AI intake.
2. Login as provider.
3. Open AI patient summaries.
4. Confirm the patient-reported symptoms, duration, urgency, summary and clinician handoff are visible.
5. Confirm the UI explicitly treats the summary as professional-review information, not a diagnosis.
6. Open patient messages.
7. Reply to the patient.
8. Confirm the patient receives the message notification.
9. Complete a provider follow-up and confirm the patient receives the completion notification.

## Backend verification

From backend:

    .\\venv\\Scripts\\Activate.ps1
    python -m alembic upgrade head
    uvicorn app.main:app --reload

Swagger: http://127.0.0.1:8000/docs

Verify these API groups: Authentication, Users, AI Assistant, Patient Care, Providers.

The admin side is intentionally excluded from these phases.
