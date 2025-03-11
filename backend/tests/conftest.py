# /home/heinrich/projects/ConsciousFit/backend/tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db import Base
from config import app_config
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="session")
def db_engine():
    """
    Returns a SQLAlchemy engine for the test database.
    """
    engine = create_engine(app_config.get_database_url())
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(db_engine):
    """
    Returns a SQLAlchemy session for the test database.
    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@pytest.fixture(scope="module")
def client():
    """
    Return a TestClient for testing the app
    """
    with TestClient(app) as client:
        yield client
