# /tests/routers/test_health.py
from fastapi.testclient import TestClient
from fastapi import status
import os
import sys
import pytest

# Adjust the path to include the 'app' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'app'))

if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from main import app
from config import app_config

client = TestClient(app)

def test_get_health_ok():
    """Test that the /health endpoint returns an OK status when the database connection is successful and the application is running correctly."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "app": {"status": "ok", "version": app_config.APP_VERSION},
        "auth": {"status": "ok", "detail": None},
        "database": {"status": "ok", "db_type": "mysql", "detail": None},
        "version": app_config.APP_VERSION
    }
