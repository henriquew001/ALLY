from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from sqlalchemy import text
import logging
from sqlalchemy.exc import ProgrammingError
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)
router = APIRouter()
from fastapi import APIRouter

router = APIRouter()

class DbHealth(BaseModel):
    """Represents the health status of the database."""
    status: str = Field(..., description="The status of the database connection (ok or error)")
    detail: str | None = Field(default=None, description="Details about the error, if any")

class AppHealth(BaseModel):
    """Represents the health status of the app."""
    status: str = Field("ok", description="The status of the application (always 'ok' in this case)")

class HealthStatus(BaseModel):
    """Represents the overall health status of the application."""
    app: AppHealth = Field(..., description="The health status of the app.")
    database: DbHealth = Field(..., description="The health status of the database connection")

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

@router.get("/health", response_model=HealthStatus)
async def get_health(db: Session = Depends(get_db)):
    """
    Returns the overall status of the application, including the database connection.
    """
    db_status = await check_db_health(db)
    app_status = AppHealth(status="ok")

    overall_status = HealthStatus(app=app_status, database=db_status)
    return overall_status
