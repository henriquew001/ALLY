# /tests/routers/test_db_info.py
from fastapi.testclient import TestClient
import pytest
import logging
import os
import sys
from sqlalchemy.orm import Session

# Adjust the path to include the 'app' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'app'))

if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from main import app
from database.db import get_db

@pytest.fixture(scope="module")
def client():
    """
    Creates a test client without dependency override
    """
    client = TestClient(app)
    yield client

def test_get_db_version_success(client: TestClient, caplog):
    caplog.set_level(logging.INFO)
    response = client.get("/db_version")
    assert response.status_code == 200, response.text

@pytest.fixture(scope="module")
def client_override(db: Session):
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

def test_get_db_version_success_sqlite(client_override: TestClient, caplog):
    """Test that the db version can be accessed"""
    caplog.set_level(logging.INFO)
    response = client_override.get("/db_version")
    assert response.status_code == 200
    assert "version" in response.json()
