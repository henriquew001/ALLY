import pymysql
import os
from fastapi import HTTPException
import logging

# Logger initialisieren
logger = logging.getLogger(__name__)

def get_db_connection():
    try:
        connection = pymysql.connect(
            host=os.environ.get("DB_HOST"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME"),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        logger.info("Database connection established")  # Log-Nachricht hinzufügen
        return connection
    except pymysql.MySQLError as e:
        logger.error(f"Database connection error: {e}") # Log-Nachricht mit Fehler
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")
