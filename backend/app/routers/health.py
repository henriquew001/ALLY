from fastapi import APIRouter
from database.db import get_db_connection  # Importiere deine Datenbankfunktion

router = APIRouter()

@router.get("/health")
async def healthcheck():
    try:
        conn = get_db_connection()
        if conn is None:
            return {"status": "error", "details": "Database connection error"}
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
        conn.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
