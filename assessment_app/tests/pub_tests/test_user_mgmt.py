import pytest
from fastapi.testclient import TestClient
from assessment_app.main import app

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "email": "testuser@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "testpassword"
    }


def test_register_user(test_user):
    response = client.post("/register", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["first_name"] == test_user["first_name"]
    assert data["last_name"] == test_user["last_name"]
