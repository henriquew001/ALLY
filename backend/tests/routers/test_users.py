# /tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
from sqlalchemy.pool import StaticPool

# Adjust the path to include the 'app' directory
current_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.abspath(os.path.join(current_dir, '..', 'app'))

if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from database.db import Base

# Use an in-memory SQLite database for testing
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def db():
    """
    Provide a database session for testing.
    """
    session = TestingSessionLocal()
    # Create the tables in the testing database
    Base.metadata.create_all(bind=engine)
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function", autouse=True)
def reset_db(db):
    """
    Resets the database by removing all data.
    """
    # clear all data
    for table in reversed(Base.metadata.sorted_tables):
      db.execute(table.delete())
    db.commit()
    yield
    # clear all data
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
