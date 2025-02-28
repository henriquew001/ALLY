from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError
import time
import sys
import os
import pytest

# Adjust the path to include the 'app' directory
# Calculate the path to the 'app' directory relative to the test file
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.abspath(os.path.join(current_dir, '..', '..', 'app'))

# Check if 'app' is already in sys.path to avoid adding it multiple times
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

# Set environment variables for testing if not already set
if not os.environ.get("SECRET_KEY"):
    os.environ["SECRET_KEY"] = "test_secret_key"
if not os.environ.get("ENV"):
    os.environ["ENV"] = "test"

from main import app  # Now import directly
from database.db import Base, get_db
from config import config


# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = config.get_database_url()

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to create tables with retry mechanism
def create_tables_with_retry(retries=3, delay=1):
    for attempt in range(retries):
        try:
            Base.metadata.create_all(bind=engine)
            return True  # Success
        except OperationalError as e:
            if attempt < retries - 1:
                print(f"Attempt {attempt + 1} to create tables failed: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Failed to create tables after {retries} attempts: {e}")
                return False  # Failure

# Create tables with retry
if not create_tables_with_retry():
    raise RuntimeError("Failed to create database tables during test setup")

@pytest.fixture(scope="function", name="db") # Geändert
def override_get_db():
    # Create the tables
    Base.metadata.create_all(bind=engine)

    # Create a new session for each test
    session: Session = TestingSessionLocal()
    yield session

    # Clear the database after each test
    session.close()
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_login_for_access_token_ok(db): # db hier genutzt
    # Create a user
    response_create = client.post("/users/", json={"username": "testuser", "password": "password"})
    assert response_create.status_code == 201
    response = client.post("/auth/token", data={"username": "testuser", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_for_access_token_wrong_credentials(db): # db hier genutzt
    response = client.post("/auth/token", data={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

def test_refresh_token(db): # db hier genutzt
    # Create a user
    response_create = client.post("/users/", json={"username": "testuser", "password": "password"})
    assert response_create.status_code == 201
    response_token = client.post("/auth/token", data={"username": "testuser", "password": "password"})
    refresh_token = response_token.json()["refresh_token"]
    headers = {"Authorization": f"Bearer {refresh_token}"}
    response = client.post("/auth/refresh", headers=headers)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_refresh_token_wrong_token(db): # db hier genutzt
    headers = {"Authorization": "Bearer wrongtoken"}
    response = client.post("/auth/refresh", headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"
