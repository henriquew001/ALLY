from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from database.db import get_db

router = APIRouter(prefix="/db_version", tags=["db_version"])


@router.get("")
def get_db_version(db: Session = Depends(get_db)):
    """Get db version"""
    try:
        result = db.execute(text("SELECT sqlite_version()")).scalar()
        return {"db_version": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
