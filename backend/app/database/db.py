from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError, ProgrammingError
from fastapi import HTTPException
from dotenv import load_dotenv  # Import load_dotenv
import os
import logging

# Load environment variables from .env
load_dotenv(dotenv_path="/app/.env") # Pfad zur .env Datei

logger = logging.getLogger(__name__)

# Datenbankverbindungsinformationen aus Umgebungsvariablen lesen
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_DATABASE") # Geändert: DB_DATABASE
SECRET_KEY = os.environ.get("SECRET_KEY")

if not all([DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, SECRET_KEY]):
    raise ValueError("Not all environment variables are set!")

# Datenbank-URL erstellen
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Engine erstellen
try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    logger.info("Database engine created")
except OperationalError as e:
    logger.error(f"Database connection error: {e}")
    raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

# Erstelle die Base Klasse
Base = declarative_base()

# Session erstellen
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency Injection für FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
        logger.info("Database session retrieved")
    finally:
        db.close()
        logger.info("Database session closed")
