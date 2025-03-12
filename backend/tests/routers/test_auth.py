# # /tests/routers/test_auth.py
# from fastapi.testclient import TestClient
# from sqlalchemy.orm import Session
# import os
# import sys
# import pytest

# # Adjust the path to include the 'app' directory
# current_dir = os.path.dirname(os.path.abspath(__file__))
# app_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'app'))

# if app_dir not in sys.path:
#     sys.path.insert(0, app_dir)

# from main import app
# from database.db import get_db

# client = TestClient(app)


# def test_login_for_access_token_fails(db: Session, monkeypatch):
#     """Test that a login attempt fails without any users."""

#     def override_get_db():
#         """Override get_db to use the test database."""
#         yield db

#     # Replace the get_db dependency with our override
#     app.dependency_overrides[get_db] = override_get_db

#     response = client.post(
#         "/auth/token",
#         data={"username": "testuser", "password": "password"},
#     )
#     assert response.status_code == 400
#     assert response.json() == {"detail": "Incorrect username or password"}

#     # Remove the override after the test
#     app.dependency_overrides.clear()
