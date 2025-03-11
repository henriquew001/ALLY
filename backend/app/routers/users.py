# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemes.user import UserCreate, User as UserScheme
from models.user import User as UserModel
from database.db import get_db
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserScheme, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user in the database.

    Args:
        user: The user data for creation.
        db: The database session.

    Returns:
        The created user.

    Raises:
        HTTPException: If the user data is invalid or if the username already exists.
    """

    db_user = UserModel(username=user.username)
    db_user.set_password(user.password)
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    logger.info(f"User {db_user.username} created")
    return db_user
