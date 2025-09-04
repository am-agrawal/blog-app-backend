from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from sqlalchemy.orm import Session
from blog_app.db.session import get_db
from blog_app.crud.blog import blog_crud
from blog_app.schemas.blog import BlogCreate, BlogResponse, BlogWithoutBody
from blog_app.schemas.user import UserResponse
from blog_app.dependencies import get_current_verified_user

router = APIRouter()


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_blog(blog_data: BlogCreate, db: Session = Depends(get_db), current_verified_user: UserResponse = Depends(get_current_verified_user)):
    """Create a new blog post."""
    blog = blog_crud.create_blog(db, current_verified_user.id, blog_data)
    return {"message": "Blog created successfully", "blog_id": blog.id}


@router.get("/blogs", response_model=List[BlogWithoutBody])
async def get_blogs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return")
):
    """Get all blog posts."""
    blogs = blog_crud.get_all_blogs(db, skip=skip, limit=limit)
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No blogs found")
    return blogs


@router.get("/{slug}", response_model=BlogResponse)
async def get_blog(slug: str, db: Session = Depends(get_db)):
    """Get a blog post by slug."""
    blog = blog_crud.get_blog_by_slug(db, slug)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog

