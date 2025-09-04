from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from blog_app.db.models.blog import Blog
from blog_app.db.models.user import User
from blog_app.schemas.blog import BlogCreate, BlogResponse, BlogWithoutBody
from blog_app.utils.blog import generate_slug


class BlogCRUD:
    def create_blog(self, db: Session, author_id: int, blog_data: BlogCreate) -> Blog:
        """Create a new blog."""
        db_blog = Blog(
            title=blog_data.title,
            excerpt=blog_data.excerpt,
            content=blog_data.content,
            author_id=author_id
        )
        db.add(db_blog)
        db.flush()
        db_blog.slug = generate_slug(blog_data.title, db_blog.id)
        db.commit()
        db.refresh(db_blog)
        return db_blog

    def get_blog_by_slug(self, db: Session, slug: str) -> BlogResponse:
        """Get a blog by slug."""
        stmt = (
            select(
                Blog.id,
                Blog.title,
                Blog.slug,
                Blog.excerpt,
                Blog.content,
                Blog.created_at,
                Blog.updated_at,
                Blog.author_id,
                User.full_name,
                User.username
            )
            .join(User, Blog.author_id == User.id)
            .filter(Blog.slug == slug, Blog.is_deleted == False)
        )
        result = db.execute(stmt).first()
        return result._asdict() if result else None

    def get_all_blogs(self, db: Session, skip: int, limit: int) -> List[BlogWithoutBody]:
        """Get all blogs."""
        stmt = (
            select(
                Blog.id,
                Blog.title,
                Blog.slug,
                Blog.excerpt,
                Blog.created_at,
                Blog.updated_at,
                Blog.author_id,
                User.full_name,
                User.username
            )
            .join(User, Blog.author_id == User.id)
            .filter(Blog.is_deleted == False)
            .offset(skip)
            .limit(limit)
        )
        
        results = db.execute(stmt).all()
        return [row._asdict() for row in results] if results else []


blog_crud = BlogCRUD()