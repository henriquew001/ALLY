# /tests/test_main.py
from fastapi.testclient import TestClient
from main import app
import pytest
from sqlalchemy import text

client = TestClient(app)

def Ftest_create_database():
    """Test that the database tables are created or already exist."""
    response = client.get("/db_version")
    assert response.status_code == 200
    assert "db_version" in response.json()

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "app": {"status": "ok"},
        "database": {"status": "ok", "detail": None},
    }

def test_create_users_endpoint():
        response = client.post("/users/", json={"username": "testuser", "password": "password"})
        assert response.status_code == 201

def test_get_token():
        response = client.post("/auth/token", data={"username": "testuser", "password": "password"})
        assert response.status_code == 200

