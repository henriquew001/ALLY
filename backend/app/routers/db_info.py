from fastapi import APIRouter, HTTPException
from database.db import get_db_connection  # Importiere deine Datenbankfunktion

router = APIRouter()

@router.get("/db_version")
async def get_db_version():
    connection = get_db_connection()
    if connection is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT VERSION()")
            result = cursor.fetchone()
            return {"MariaDB Version": result['VERSION()']}
    finally:
        connection.close()
