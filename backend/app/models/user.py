# app/models/user.py
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, Session
from database.db import Base
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

    def check_password(self, password: str):
        return pwd_context.verify(password, self.hashed_password)

    @staticmethod
    async def authenticate(username, password, db: Session):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not user.check_password(password):
            return None
        return user
