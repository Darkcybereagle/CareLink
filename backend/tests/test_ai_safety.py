from conftest import auth_header


def test_emergency_signal_has_priority(client):
    headers = auth_header(client, "patient", "emergency@carelink.test")
    response = client.post("/api/v1/ai/intake", headers=headers, json={
        "symptoms": "I have chest pain and difficulty breathing",
        "duration": "10 minutes",
    })
    assert response.status_code == 200
    assert response.json()["urgency"] == "emergency"
    assert "emergency" in response.json()["safety_message"].lower()
