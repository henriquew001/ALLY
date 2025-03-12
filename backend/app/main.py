# /app/main.py
from fastapi import FastAPI
from routers import auth, health, db_info
import logging
from database.db import engine, Base

# Create the tables
Base.metadata.create_all(bind=engine)

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# app.include_router(users.router)
app.include_router(auth.router)
app.include_router(health.router)
app.include_router(db_info.router)

@app.get("/")
async def root():
    """
    Root endpoint, returns the welcome message.
    """
    return {"message": "ConsciousFit"}
