# /tests/routers/test_db_info.py
import logging
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from database.db import get_db
from main import app as main_app  # Import the app instance from main.py


@pytest.fixture(scope="module")
def app():
    """Fixture that creates and yields the app instance"""
    return main_app


@pytest.fixture(scope="module")
def client(app: FastAPI):
    """Fixture that yields a test client for the app."""
    with TestClient(app) as c:
        yield c


def test_get_db_version_success(client: TestClient, caplog):
    caplog.set_level(logging.INFO)
    response = client.get("/db_version")
    assert response.status_code == 200
    assert response.json() == {"db_version": "10.11.6-MariaDB-1:10.11.6+maria~ubu2204"}


def test_get_db_version_fail(client: TestClient, caplog, app: FastAPI):  # add app here
    caplog.set_level(logging.ERROR)

    mock_session = MagicMock(spec=Session)
    mock_session.execute.return_value.scalar.side_effect = ProgrammingError("Fake SQL Error", {}, None)

    app.dependency_overrides[get_db] = lambda: mock_session  # Set it on the app instance from the fixture!

    # 🔍 Debugging: Prüfen, ob die Dependency-Override greift
    print("Dependency Overrides:", app.dependency_overrides)  # Sollte get_db enthalten
    print("Mock Session ID:", id(mock_session))

    response = client.get("/db_version")

    # 🔍 Prüfen, ob die Methode wirklich aufgerufen wurde
    print("Mock execute called:", mock_session.execute.called)

    assert mock_session.execute.called, "Mock wurde nicht aufgerufen!"  # Debugging
    assert response.status_code == 500
    assert "Database error" in response.text

    app.dependency_overrides.clear()  # clear overrides after the test

