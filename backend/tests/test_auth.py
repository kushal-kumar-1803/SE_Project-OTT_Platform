import json
from backend.app import app

client = app.test_client()

def test_register_user():
    response = client.post(
        "/auth/register",
        data=json.dumps({
            "name": "TestUser",
            "email": "pytest_user@example.com",
            "password": "123456"
        }),
        content_type="application/json"
    )
    assert response.status_code in [201, 409]


def test_login_valid_user():
    response = client.post(
        "/auth/login",
        data=json.dumps({
            "email": "pytest_user@example.com",
            "password": "123456"
        }),
        content_type="application/json"
    )
    assert response.status_code == 200
    assert "token" in response.json


def test_login_invalid_password():
    response = client.post(
        "/auth/login",
        data=json.dumps({
            "email": "pytest_user@example.com",
            "password": "wrong"
        }),
        content_type="application/json"
    )
    assert response.status_code == 401
