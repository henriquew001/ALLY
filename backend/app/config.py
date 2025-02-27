# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables if present

class Config:
    ENV = os.environ.get("ENV", "dev")  # Default to 'dev' if not set
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
    DATABASE_URL = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.environ.get("REFRESH_TOKEN_EXPIRE_DAYS", 30))
    ALGORITHM = os.environ.get("ALGORITHM", "HS256")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set.")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is not set.")

    def get_database_url(self) -> str:
        """
        Returns the database URL based on the environment.
        """
        return self.DATABASE_URL

config = Config()
