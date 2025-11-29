from pydantic import BaseModel
from typing import Optional
from blog_app.schemas.user import UserResponse


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse


class TokenPayload(BaseModel):
    sub: str
    user_id: int
    exp: Optional[int] = None
    type: Optional[str] = None
