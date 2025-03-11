from fastapi import status
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_health_ok():
    """Test that the /health endpoint returns an OK status when the database connection is successful and the application is running correctly."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "app": {"status": "ok"},
        "database": {"status": "ok", "detail": None},
    }
