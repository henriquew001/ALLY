from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from sqlalchemy.exc import ProgrammingError
from unittest.mock import patch, MagicMock
from fastapi import status
from database.db import get_db  # Import get_db
from app.main import app  # Import the FastAPI app

def test_get_db_version_ok(client: TestClient):
    response = client.get("/db_version")
    assert response.status_code == status.HTTP_200_OK
    assert "db_version" in response.json()

from unittest.mock import patch
import logging

def test_get_db_version_fail(client: TestClient, caplog):
    caplog.set_level(logging.ERROR)

    mock_session = MagicMock(spec=Session)
    mock_session.execute.side_effect = ProgrammingError("Fake SQL Error", {}, None)

    app.dependency_overrides[get_db] = lambda: mock_session  # Direktes Setzen!

    # 🔍 Debugging: Prüfen, ob die Dependency-Override greift
    print("Dependency Overrides:", app.dependency_overrides)  # Sollte get_db enthalten
    print("Mock Session ID:", id(mock_session))

    response = client.get("/db_version")

    # 🔍 Prüfen, ob die Methode wirklich aufgerufen wurde
    print("Mock execute called:", mock_session.execute.called)

    assert mock_session.execute.called, "Mock wurde nicht aufgerufen!"  # Debugging
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "SQL error:" in response.json().get("detail")

    del app.dependency_overrides[get_db]  # Cleanup nach Test
