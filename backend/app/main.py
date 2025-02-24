from fastapi import FastAPI, HTTPException
from database.db import get_db_connection  # Importiere die Funktion

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "ANNY & Heinrich"}

@app.get("/db_version")
async def get_db_version():
    connection = get_db_connection()  # Nutze die importierte Funktion
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            result = cursor.fetchone()
            return {"MariaDB Version": result['VERSION()']}
    finally:
        connection.close()

@app.get("/health")
async def healthcheck():
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
        conn.close()
        return {"status": "ok"}
    except Exception:
        return {"status": "error"}
