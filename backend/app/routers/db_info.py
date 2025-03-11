# app/routers/db_info.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.db import get_db

router = APIRouter()

@router.get("/db_version")
def get_db_version(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT VERSION()")).scalar()
        return {"db_version": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
