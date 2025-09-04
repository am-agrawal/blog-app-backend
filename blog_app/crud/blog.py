from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from datetime import datetime, timedelta, timezone
from blog_app.db.models.blog import Blog
from blog_app.schemas.blog import BlogCreate
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
    

blog_crud = BlogCRUD()