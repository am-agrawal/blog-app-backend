from fastapi import APIRouter, Depends, HTTPException, status, Response, BackgroundTasks
from sqlalchemy.orm import Session
from blog_app.db.session import get_db
from blog_app.crud.user import user_crud
from blog_app.schemas.user import UserCreate, UserResponse, UserLogin, OTPVerify, TokenResponse
from blog_app.core.security import create_access_token, create_refresh_token, generate_otp
from blog_app.utils.email import send_verification_email

router = APIRouter()


@router.post("/signup", response_model=dict, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """User registration endpoint."""
    # Check if user already exists
    if user_crud.get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if user_crud.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create user
    user = user_crud.create_user(db, user_data)
    
    # Generate OTP
    otp_code = generate_otp()
    user_crud.create_otp(db, user.email, otp_code)
    
    # Send verification email
    background_tasks.add_task(send_verification_email, user.email, otp_code)
    
    return {
        "message": "User registered successfully. Please check your email for verification code.",
        "user_id": user.id
    }


@router.post("/verify", response_model=dict)
async def verify_otp(otp_data: OTPVerify, db: Session = Depends(get_db)):
    """Verify OTP and mark user as verified."""
    # Verify OTP
    otp = user_crud.verify_otp(db, otp_data.email, otp_data.otp_code)
    
    if not otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Get user and mark as verified
    user = user_crud.get_user_by_email(db, otp_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    verified_user = user_crud.verify_user(db, user.id)
    
    return {
        "message": "Email verified successfully",
        "user_id": verified_user.id
    }


@router.post("/login", response_model=TokenResponse)
async def login(
    user_credentials: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
):
    """User login endpoint."""
    # Authenticate user
    user = user_crud.authenticate_user(db, user_credentials.email, user_credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please verify your email first"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is deactivated"
        )
    
    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    # Set cookies
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=1800
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=604800
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse.from_orm(user)
    )


@router.post("/logout")
async def logout(response: Response):
    """User logout endpoint."""
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    
    return {"message": "Logged out successfully"} 