from conftest import auth_header


def test_emergency_signal_has_priority(client):
    headers = auth_header(client, "patient", "emergency@carelink.example.com")
    response = client.post("/api/v1/ai/intake", headers=headers, json={
        "symptoms": "I have chest pain and difficulty breathing",
        "duration": "10 minutes",
    })
    assert response.status_code == 200
    assert response.json()["urgency"] == "emergency"
    assert "emergency" in response.json()["safety_message"].lower()


def test_serious_bleeding_is_emergency(client):
    headers = auth_header(client, "patient", "bleeding-emergency@carelink.example.com")
    response = client.post("/api/v1/ai/intake", headers=headers, json={
        "symptoms": "I have serious bleeding from my nose and it is still bleeding",
        "duration": "2 days",
    })
    assert response.status_code == 200
    assert response.json()["urgency"] == "emergency"


def test_provider_cannot_submit_patient_ai_intake(client):
    headers = auth_header(client, "nurse", "nurse-ai-access@carelink.example.com")
    response = client.post("/api/v1/ai/intake", headers=headers, json={
        "symptoms": "headache", "duration": "1 day",
    })
    assert response.status_code == 403
