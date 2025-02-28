from fastapi import FastAPI
from routers import health, db_info, users, auth
from database.db import Base, engine
import logging
from config import config
import os
import time
from sqlalchemy.exc import OperationalError
from sqlalchemy import text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting FastAPI application")

app = FastAPI()

# Include routers
app.include_router(health.router)
app.include_router(db_info.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.on_event("startup")
async def on_startup():
    """
    Creates the database tables if they do not exist.
    Retries multiple times with a delay if the connection fails.
    """
    if config.ENV == "dev":
        MAX_RETRIES = 10
        RETRY_DELAY = 3
        retries = 0
        while retries < MAX_RETRIES:
            try:
                Base.metadata.create_all(bind=engine)
                logger.info("Database tables created or already exist.")
                break
            except OperationalError as e:
                logger.error(f"Database connection failed, retrying in {RETRY_DELAY} seconds, attempt {retries + 1}: {e}")
                retries += 1
                time.sleep(RETRY_DELAY)
            except Exception as e:
                logger.error(f"Unexpected error connecting to the database: {e}")
                break  # Stop retrying on unexpected errors

