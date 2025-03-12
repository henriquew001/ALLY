# /home/heinrich/projects/ConsciousFit/backend/tests/routers/test_health.py
from fastapi.testclient import TestClient
from fastapi import status
import os
import sys
import pytest
from sqlalchemy.orm import Session

# Adjust the path to include the 'app' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'app'))

if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from main import app
from database.db import get_db

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

def test_get_health_ok(test_client: TestClient):
    """Test that the /health endpoint returns an OK status."""
    response = test_client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "ok"}
