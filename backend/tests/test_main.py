# /tests/test_main.py
from fastapi.testclient import TestClient
import os
import sys
import pytest

# Adjust the path to include the 'app' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.abspath(os.path.join(current_dir, '..', 'app'))

if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from main import app
from database.db import get_db
from sqlalchemy.orm import Session

@pytest.fixture(scope="module")
def test_client(db: Session):
    """
    Overrides the get_db dependency for all tests in this module.
    """

    async def override_get_db():
        """Override get_db to use the test database."""
        yield db

    # Replace the get_db dependency with our override
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    # Remove the override after the test
    app.dependency_overrides.clear()
    

def test_read_main(test_client: TestClient):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "ConsciousFit"}

def test_create_users_endpoint(test_client: TestClient, reset_db):
    response = test_client.post("/users/", json={"username": "testuser", "password": "password"})
    assert response.status_code == 201

def test_create_users_duplicate_endpoint(test_client: TestClient, reset_db):
    test_client.post("/users/", json={"username": "testuser", "password": "password"})
    response = test_client.post("/users/", json={"username": "testuser", "password": "password"})
    assert response.status_code == 400

