# /app/routers/db_info.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
import logging
from sqlalchemy import text, inspect

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/db_version", tags=["Database Version"])


@router.get("/")
async def get_db_version(db: Session = Depends(get_db)):
    """
    Returns the database version.
    """
    try:
        inspector = inspect(db.bind)
        if inspector.dialect.name == "sqlite":
            version_query = text("SELECT sqlite_version()")
        elif inspector.dialect.name == "mysql":
            version_query = text("SELECT version()")
        else:
            raise ValueError("Unsupported database type")

        result = db.execute(version_query).scalar()
        return {"version": result}

    except Exception as e:
        logger.error(f"Database error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {e}"
        )
