from fastapi import FastAPI, HTTPException
import pymysql
import os

app = FastAPI()

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
        return connection
    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

@app.get("/")
async def read_root():
    return {"Hello": "ANNY & Heinrich "}

@app.get("/db_version")
async def get_db_version():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            result = cursor.fetchone()
            return {"MariaDB Version": result['VERSION()']}
    finally:
        connection.close()

@app.get("/health")  # Add a healthcheck endpoint
async def healthcheck():
  try:
      conn = get_db_connection()
      with conn.cursor() as cursor:
          cursor.execute("SELECT 1")
      conn.close()
      return {"status": "ok"}
  except Exception:
    return {"status": "error"}
