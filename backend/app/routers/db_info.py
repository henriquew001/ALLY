from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text  # Für rohe SQL-Abfragen
from database.db import get_db

router = APIRouter()

@router.get("/db_version")
async def get_db_version(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT VERSION()"))
        version = result.fetchone()[0]  # Das Ergebnis ist ein Tupel
        return {"MariaDB Version": version}
    except ProgrammingError as e:  # Spezifischer für SQL-Fehler
        logger.error(f"SQL error: {e}")
        raise HTTPException(status_code=500, detail=f"SQL error: {e}")
