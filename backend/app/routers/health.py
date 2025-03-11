# /app/routers/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from sqlalchemy import text, inspect
import logging
from sqlalchemy.exc import ProgrammingError, OperationalError
from pydantic import BaseModel, Field
from config import app_config
from models.user import User as UserModel

logger = logging.getLogger(__name__)
router = APIRouter()

class DbHealth(BaseModel):
    """Represents the health status of the database."""
    status: str = Field(..., description="The status of the database connection (ok or error)")
    db_type: str | None = Field(default=None, description="The type of the database (mysql or sqlite)")
    detail: str | None = Field(default=None, description="Details about the error, if any")

class AuthHealth(BaseModel):
    """Represents the health status of the authentication."""
    status: str = Field(..., description="The status of the authentication (ok or error)")
    detail: str | None = Field(default=None, description="Details about the error, if any")

class AppHealth(BaseModel):
    """Represents the health status of the app."""
    status: str = Field("ok", description="The status of the application (always 'ok' in this case)")
    version: str = Field("1.0.0", description="The version of the app")

class HealthStatus(BaseModel):
    """Represents the overall health status of the application."""
    app: AppHealth = Field(..., description="The health status of the app.")
    auth: AuthHealth = Field(..., description="The health status of the auth.")
    database: DbHealth = Field(..., description="The health status of the database connection")
    version: str = Field(..., description="The version of the app.")

async def check_db_health(db: Session) -> DbHealth:
    """Helper function to check the database connection."""
    try:
        inspector = inspect(db.bind)
        if inspector.dialect.name == "sqlite":
            db_type = "sqlite"
        elif inspector.dialect.name == "mysql":
            db_type = "mysql"
        else:
            db_type = "unknown"
        db.execute(text("SELECT 1"))
        return DbHealth(status="ok", db_type=db_type)
    except ProgrammingError as e:
        logger.error(f"db_health error: {e}")
        return DbHealth(status="error", detail=str(e))
    except Exception as e:
        logger.error(f"db_health unexpected error: {e}")
        return DbHealth(status="error", detail=str(e))

async def check_auth_health(db: Session) -> AuthHealth:
    """Helper function to check the database connection."""
    try:
        user_count = db.query(UserModel).count()
        return AuthHealth(status="ok")
    except OperationalError as e:
        logger.error(f"auth_health OperationalError: {e}")
        return AuthHealth(status="error", detail=str(e))
    except Exception as e:
        logger.error(f"auth_health unexpected error: {e}")
        return AuthHealth(status="error", detail=str(e))


@router.get("/health", response_model=HealthStatus)
async def get_health(db: Session = Depends(get_db)):
    """
    Returns the overall status of the application, including the database connection.
    """
    db_status = await check_db_health(db)
    auth_status = await check_auth_health(db)
    app_status = AppHealth(status="ok", version=app_config.APP_VERSION)

    overall_status = HealthStatus(app=app_status, auth=auth_status, database=db_status, version=app_config.APP_VERSION)
    return overall_status
