from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.db.models import ProviderProfile, VerificationStatus
from conftest import TestingSessionLocal, auth_header


def test_patient_provider_end_to_end(client):
    patient_headers = auth_header(client, "patient", "patient-flow@carelink.example.com")
    profile = client.post("/api/v1/users/me/patient-profile", headers=patient_headers, json={
        "phone": "+2348000000000", "gender": "unspecified", "address": "Abuja, Nigeria",
    })
    assert profile.status_code == 201, profile.text

    intake = client.post("/api/v1/ai/intake", headers=patient_headers, json={
        "symptoms": "I have had a mild headache", "duration": "2 hours",
    })
    assert intake.status_code == 200, intake.text
    assert intake.json()["urgency"] == "routine"

    provider_headers = auth_header(client, "nurse", "nurse-flow@carelink.example.com")
    provider = client.get("/api/v1/users/me", headers=provider_headers).json()
    created = client.post("/api/v1/providers/me/profile", headers=provider_headers, json={
        "provider_type": "nurse", "specialty": "Community health",
        "license_number": "TEST-NURSE-001", "phone": "+2348111111111",
        "facility_name": "CareLink Test Facility", "city": "Abuja",
        "bio": "Integration-test provider profile.",
    })
    assert created.status_code == 201, created.text

    with TestingSessionLocal() as db:
        row = db.scalar(select(ProviderProfile).where(ProviderProfile.user_id == provider["id"]))
        row.verification_status = VerificationStatus.VERIFIED
        db.commit()

    providers = client.get("/api/v1/care/providers?city=Abuja", headers=patient_headers)
    assert providers.status_code == 200
    assert any(item["id"] == provider["id"] for item in providers.json())

    nurses = client.get("/api/v1/care/providers?city=Abuja&provider_type=nurse", headers=patient_headers)
    assert nurses.status_code == 200
    assert any(item["id"] == provider["id"] and item["provider_type"] == "nurse" for item in nurses.json())

    doctors = client.get("/api/v1/care/providers?city=Abuja&provider_type=doctor", headers=patient_headers)
    assert doctors.status_code == 200
    assert all(item["provider_type"] == "doctor" for item in doctors.json())

    scheduled = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()
    appointment = client.post("/api/v1/care/appointments", headers=patient_headers, json={
        "provider_id": provider["id"], "scheduled_at": scheduled, "reason": "Follow-up assessment",
    })
    assert appointment.status_code == 201, appointment.text
    appointment_id = appointment.json()["id"]

    provider_appointments = client.get("/api/v1/providers/appointments", headers=provider_headers)
    assert provider_appointments.status_code == 200
    assert any(item["id"] == appointment_id for item in provider_appointments.json())

    updated = client.patch(f"/api/v1/providers/appointments/{appointment_id}/status",
        headers=provider_headers, json={"status": "confirmed"})
    assert updated.status_code == 200, updated.text
    assert updated.json()["status"] == "confirmed"

    thread = client.post("/api/v1/care/threads", headers=patient_headers, json={"provider_id": provider["id"]})
    assert thread.status_code == 201, thread.text
    thread_id = thread.json()["id"]
    sent = client.post(f"/api/v1/care/threads/{thread_id}/messages", headers=patient_headers,
        json={"body": "Hello, I have a question before the appointment."})
    assert sent.status_code == 201, sent.text
    provider_threads = client.get("/api/v1/providers/threads", headers=provider_headers)
    assert provider_threads.status_code == 200, provider_threads.text
    assert any(item["id"] == thread_id for item in provider_threads.json())


def test_provider_availability_validation(client):
    headers = auth_header(client, "doctor", "doctor-availability@carelink.example.com")
    response = client.post("/api/v1/providers/me/availability", headers=headers, json={
        "day_of_week": 1, "start_time": "17:00:00", "end_time": "09:00:00",
    })
    assert response.status_code == 400
