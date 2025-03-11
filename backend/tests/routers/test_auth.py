# /tests/routers/test_auth.py
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import os
import sys
import pytest

# Adjust the path to include the 'app' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'app'))

if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from main import app
from models.user import User as UserModel
from database.db import get_db

client = TestClient(app)

def test_login_for_access_token_ok(db: Session, reset_db, monkeypatch):
    """Test that a user can be created"""

    def override_get_db():
        """Override get_db to use the test database."""
        yield db

    # Replace the get_db dependency with our override
    app.dependency_overrides[get_db] = override_get_db

    # Create a user
    response_create = client.post("/users/", json={"username": "testuser", "password": "password"})
    assert response_create.status_code == 201
    # check if user is created in db
    user = db.query(UserModel).filter(UserModel.username == "testuser").first()
    assert user.username == "testuser"
    # delete User from the db
    db.delete(user)
    db.commit()
    assert db.query(UserModel).filter(UserModel.username == "testuser").first() is None

    # Remove the override after the test
    app.dependency_overrides.clear()

