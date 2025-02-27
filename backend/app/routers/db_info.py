from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text  # Für rohe SQL-Abfragen
from database.db import get_db
import logging
from sqlalchemy.exc import ProgrammingError

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/db_version")
async def get_db_version(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT VERSION()")) # use text()
        version = result.fetchone()[0]  # Das Ergebnis ist ein Tupel
        return {"MariaDB Version": version}
    except ProgrammingError as e:  # Spezifischer für SQL-Fehler
        logger.error(f"SQL error: {e}")
        raise HTTPException(status_code=500, detail=f"SQL error: {e}")
    except Exception as e:
        logger.error(f"unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"unexpected error: {e}")
