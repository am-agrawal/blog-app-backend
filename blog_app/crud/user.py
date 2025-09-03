from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from datetime import datetime, timedelta, timezone
from blog_app.db.models.user import User, OTP
from blog_app.schemas.user import UserCreate
from blog_app.core.security import get_password_hash, verify_password


class UserCRUD:
    def create_user(self, db: Session, user_data: UserCreate) -> User:
        """Create a new user."""
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password,
            verified=False
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()
    
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()
    
    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password."""
        user = self.get_user_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
    
    def verify_user(self, db: Session, user_id: int) -> Optional[User]:
        """Mark user as verified."""
        user = self.get_user_by_id(db, user_id)
        if user:
            user.verified = True
            db.commit()
            db.refresh(user)
        return user
    
    def create_otp(self, db: Session, email: str, otp_code: str, expires_in_minutes: int = 10) -> OTP:
        """Create a new OTP for email verification."""
        # Invalidate any existing OTPs for this email
        db.query(OTP).filter(OTP.email == email).update({"is_used": True})

        expires_at = datetime.now(timezone.utc) + timedelta(minutes=expires_in_minutes)
        db_otp = OTP(
            email=email,
            otp_code=otp_code,
            expires_at=expires_at
        )
        db.add(db_otp)
        db.commit()
        db.refresh(db_otp)
        return db_otp
    
    def verify_otp(self, db: Session, email: str, otp_code: str) -> Optional[OTP]:
        """Verify OTP for email verification."""
        current_time = datetime.now(timezone.utc)
        otp = db.query(OTP).filter(
            and_(
                OTP.email == email,
                OTP.otp_code == otp_code,
                OTP.is_used == False,
                OTP.expires_at > current_time
            )
        ).first()
        
        if otp:
            otp.is_used = True
            db.commit()
            db.refresh(otp)
            return otp
        return None
    
    def get_active_otp(self, db: Session, email: str) -> Optional[OTP]:
        """Get active OTP for email."""
        current_time = datetime.now(timezone.utc)
        return db.query(OTP).filter(
            and_(
                OTP.email == email,
                OTP.is_used == False,
                OTP.expires_at > current_time
            )
        ).first()


user_crud = UserCRUD() 