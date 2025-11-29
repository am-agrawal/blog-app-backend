from typing import Optional
from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.orm import Session
from blog_app.core.security import verify_token
from blog_app.core.config import settings
from blog_app.crud.user import user_crud
from blog_app.db.session import get_db


def get_current_user(
    access_token: Optional[str] = Cookie(None, alias=settings.ACCESS_TOKEN_COOKIE_NAME),
    db: Session = Depends(get_db)
):
    """Get current user from JWT token in cookie."""
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    payload = verify_token(access_token, "access")
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    user_id = payload.user_id
    
    user = user_crud.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user


def get_current_active_user(current_user = Depends(get_current_user)):
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def get_current_verified_user(current_user = Depends(get_current_user)):
    """Get current verified user."""
    if not current_user.verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not verified"
        )
    return current_user 