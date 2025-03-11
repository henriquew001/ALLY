from fastapi.testclient import TestClient
import pytest
from database.db import get_db, Base, engine
from main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine  # Import create_engine
import os
from config import app_config

# Create a test database (in-memory SQLite for testing)
if app_config.ENV == "test":
    TEST_DATABASE_URL = "sqlite:///./test.db"
    if os.path.exists(TEST_DATABASE_URL.replace("sqlite:///", "")):
        os.remove(TEST_DATABASE_URL.replace("sqlite:///", ""))
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)

else:
    TEST_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override the dependency to use the test database."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the get_db dependency in your main app
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def reset_db():
    """Reset the database state after each test."""
    session = TestingSessionLocal()
    yield
    # Delete all data after each test.
    for table in reversed(Base.metadata.sorted_tables):
        try:
            session.execute(table.delete())
        except Exception as e:
            pass
    session.commit()
    session.close()
