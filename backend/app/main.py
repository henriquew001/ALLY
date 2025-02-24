from fastapi import FastAPI
from routers import health, db_info  # Importiere die Router

app = FastAPI()

app.include_router(health.router)  # Füge den Health-Check-Router hinzu
app.include_router(db_info.router)  # Füge den DB-Info-Router hinzu

@app.get("/")
async def read_root():
    return {"Hello": "ANNY & Heinrich"}
