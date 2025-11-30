from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List
from blog_app.db.models.blog import Blog
from blog_app.db.models.user import User
from blog_app.schemas.blog import BlogCreate, BlogResponse, BlogWithoutBody, BlogUpdate
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
        base_query = db.query(
                    Blog.id,
                    Blog.title,
                    Blog.slug,
                    Blog.excerpt,
                    Blog.created_at,
                    Blog.updated_at,
                    Blog.author_id,
                    User.full_name,
                    User.username
                ).join(
                    User, Blog.author_id == User.id
                ).filter(
                    Blog.is_deleted == False
                )

        total_count = base_query.count()

        blogs = base_query.offset(skip).limit(limit).all()

        return [row._asdict() for row in blogs] if blogs else [], total_count

    def delete_blog(self, db: Session, blog_id: int) -> None:
        """Delete a blog."""
        stmt = (
            select(Blog)
            .filter(Blog.id == blog_id)
        )
        result = db.execute(stmt).scalar_one_or_none()
        if result:
            result.is_deleted = True
            db.commit()
    
    def update_blog(self, db: Session, blog_id: int, blog_data: BlogUpdate) -> Blog:
        """Update a blog."""
        stmt = (
            select(Blog)
            .filter(Blog.id == blog_id, Blog.is_deleted == False)
        )
        db_blog = db.execute(stmt).scalar_one_or_none()
        if db_blog:
            db_blog.title = blog_data.title
            db_blog.excerpt = blog_data.excerpt
            db_blog.content = blog_data.content
            db.commit()
            db.refresh(db_blog)
        return db_blog

blog_crud = BlogCRUD()