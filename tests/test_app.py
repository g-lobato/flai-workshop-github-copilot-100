import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200 or response.status_code == 307
    # Should redirect to /static/index.html
    assert str(response.url).endswith("/static/index.html")

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_unregister_activity():
    # Use a known activity from the app (e.g., "chess")
    activity = next(iter(client.get("/activities").json().keys()))
    email = "testuser@example.com"

    # Signup
    signup_url = f"/activities/{activity}/signup"
    response = client.post(signup_url, params={"email": email})
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(signup_url, params={"email": email})
    assert response.status_code == 400

    # Unregister
    unregister_url = f"/activities/{activity}/unregister"
    import json
    response = client.request(
        "DELETE",
        unregister_url,
        data=json.dumps({"email": email}),
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    assert f"Unregistered {email}" in response.json()["message"]

    # Unregister again should fail
    response = client.request(
        "DELETE",
        unregister_url,
        data=json.dumps({"email": email}),
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 400
