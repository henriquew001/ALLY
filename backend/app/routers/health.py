from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db  # Korrekter Import

router = APIRouter()

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Überprüfen der Datenbankverbindung
        db.execute("SELECT 1")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
