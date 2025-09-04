from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from blog_app.db.session import get_db
from blog_app.crud.blog import blog_crud
from blog_app.schemas.blog import BlogCreate
from blog_app.schemas.user import UserResponse
from blog_app.dependencies import get_current_verified_user

router = APIRouter()


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_blog(blog_data: BlogCreate, db: Session = Depends(get_db), current_verified_user: UserResponse = Depends(get_current_verified_user)):
    """Create a new blog post."""
    blog = blog_crud.create_blog(db, current_verified_user.id, blog_data)
    return {"message": "Blog created successfully", "blog_id": blog.id}

