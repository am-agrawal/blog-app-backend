from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from sqlalchemy.orm import Session
from blog_app.db.session import get_db
from blog_app.crud.blog import blog_crud
from blog_app.schemas.blog import BlogCreate, BlogResponse, BlogUpdate, GetAllBlogsResponse
from blog_app.schemas.user import UserResponse
from blog_app.dependencies import get_current_verified_user

router = APIRouter()


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog_data: BlogCreate, 
    db: Session = Depends(get_db), 
    current_verified_user: UserResponse = Depends(get_current_verified_user)
):
    """Create a new blog post."""
    blog = blog_crud.create_blog(db, current_verified_user.id, blog_data)
    return {"message": "Blog created successfully", "blog_id": blog.id}


@router.get("/", response_model=GetAllBlogsResponse)
async def get_blogs(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return")
):
    """Get all blog posts."""
    blogs, total_count = blog_crud.get_all_blogs(db, skip=skip, limit=limit)
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No blogs found")
    return GetAllBlogsResponse(blogs=blogs, total_count=total_count)


@router.get("/{slug}", response_model=BlogResponse)
async def get_blog(slug: str, db: Session = Depends(get_db)):
    """Get a blog post by slug."""
    blog = blog_crud.get_blog_by_slug(db, slug)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog


@router.delete("/{slug}", response_model=dict)
async def delete_blog(
    slug: str, 
    db: Session = Depends(get_db), 
    current_verified_user: UserResponse = Depends(get_current_verified_user)
):
    """Delete a blog post by slug."""
    blog = blog_crud.get_blog_by_slug(db, slug)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    if blog.get('author_id') != current_verified_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this blog")
    blog_crud.delete_blog(db, blog.get('id'))
    return {"message": "Blog deleted successfully"}


@router.put("/{slug}", response_model=dict)
async def update_blog(
    slug: str, 
    blog_data: BlogUpdate, 
    db: Session = Depends(get_db), 
    current_verified_user: UserResponse = Depends(get_current_verified_user)
):
    """Update a blog post by slug."""
    blog = blog_crud.get_blog_by_slug(db, slug)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    if blog.get('author_id') != current_verified_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this blog")
    blog_crud.update_blog(db, blog.get('id'), blog_data)
    return {"message": "Blog updated successfully"}
