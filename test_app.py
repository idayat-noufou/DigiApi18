from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_get_clients():
    response = client.get("/api/v1/client")
    assert response.status_code == 200


def test_create_client():
    payload = {
        "nom": "Test",
        "prenom": "User",
        "adresse": "123 Rue Test"
    }
    response = client.post("/api/v1/client", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "codcli" in data
    return data["codcli"]


def test_get_client_by_id():
    client_id = test_create_client()
    response = client.get(f"/api/v1/client/{client_id}")
    assert response.status_code == 200


def test_patch_client():
    client_id = test_create_client()
    response = client.patch(
        f"/api/v1/client/{client_id}",
        json={"prenom": "Updated"}
    )
    assert response.status_code == 200


def test_delete_client():
    client_id = test_create_client()
    response = client.delete(f"/api/v1/client/{client_id}")
    assert response.status_code == 200
