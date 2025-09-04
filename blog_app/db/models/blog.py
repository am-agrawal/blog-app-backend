import random
from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey, DateTime, func, event
from sqlalchemy.orm import relationship
from blog_app.db.base import Base
from blog_app.utils.blog import generate_slug

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=True)
    
    excerpt = Column(String(500), nullable=True)
    
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    is_deleted = Column(Boolean, default=False)

    author = relationship("User", back_populates="blogs")


@event.listens_for(Blog, "before_insert")
def generate_slug_before_insert(mapper, connection, target):
    if not target.slug:
        target.slug = generate_slug(target.title, random.randint(1, 10000))
