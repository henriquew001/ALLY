# /home/heinrich/projects/ConsciousFit/backend/tests/routers/test_db_info.py
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from sqlalchemy.exc import ProgrammingError
from unittest.mock import patch
from fastapi import status

def test_get_db_version_ok(db: Session, client: TestClient):
    response = client.get("/db_version")
    assert response.status_code == status.HTTP_200_OK
    assert "MariaDB Version" in response.json()

def test_get_db_version_fail(db: Session, client: TestClient, monkeypatch):
    def mock_db_execute(*args, **kwargs):
        raise ProgrammingError("Fake SQL Error", {}, None)
    
    monkeypatch.setattr(db, "execute", mock_db_execute)
    response = client.get("/db_version")
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "SQL error" in response.json().get("detail")
