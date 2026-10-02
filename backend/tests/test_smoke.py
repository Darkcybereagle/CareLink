from conftest import auth_header


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register_login_and_me(client):
    headers = auth_header(client, "patient")
    me = client.get("/api/v1/users/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["role"] == "patient"
    login = client.post("/api/v1/auth/login", json={"email": "patient@carelink.test", "password": "StrongPass123!"})
    assert login.status_code == 200
    assert login.json()["token_type"] == "bearer"


def test_role_access_is_enforced(client):
    patient = auth_header(client, "patient")
    response = client.get("/api/v1/providers/me", headers=patient)
    assert response.status_code == 403
