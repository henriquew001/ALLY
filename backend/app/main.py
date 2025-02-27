from fastapi import FastAPI
from routers import health, db_info, users, auth
from database.db import Base, engine
import logging
import os

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

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

