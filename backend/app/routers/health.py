# /app/routers/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from sqlalchemy import text, inspect
import logging
from sqlalchemy.exc import ProgrammingError
from pydantic import BaseModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["Health"])

class DbHealth(BaseModel):
    """Represents the health status of the database."""
    status: str = "ok"
    detail: str | None = None

class AppHealth(BaseModel):
    """Represents the health status of the app."""
    status: str = "ok"
    version: str = "1.0.0"

class HealthStatus(BaseModel):
    """Represents the overall health status of the application."""
    app: AppHealth = AppHealth()
    database: DbHealth = DbHealth()
    version: str = "1.0.0"

async def check_db_health(db: Session) -> DbHealth:
    """Helper function to check the database connection."""
    try:
        db.execute(text("SELECT 1"))
        return DbHealth(status="ok")
    except ProgrammingError as e:
        logger.error(f"db_health error: {e}")
        return DbHealth(status="error", detail=str(e))
    except Exception as e:
        logger.error(f"db_health unexpected error: {e}")
        return DbHealth(status="error", detail=str(e))

@router.get("")
async def get_health(db: Session = Depends(get_db)):
    """
    Returns the overall status of the application, including the database connection.
    """
    db_status = await check_db_health(db)
    return {"status": "ok"}

