from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text  # Import text()
from database.db import get_db
import logging
from sqlalchemy.exc import ProgrammingError, DatabaseError # Import DatabaseError
from fastapi import status

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/db_version")
async def get_db_version(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT VERSION()")).fetchone()  # Use text() here
        db_version = result[0]
        return {"db_version": db_version}
    except ProgrammingError as e:  # Spezifischer für SQL-Fehler
        logger.error(f"SQL error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"SQL error: {e}")
    except DatabaseError as e:
        logger.error(f"DB error {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    except Exception as e:
        logger.error(f"unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"unexpected error: {e}")
