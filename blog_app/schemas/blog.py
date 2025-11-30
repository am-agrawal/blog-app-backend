from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class BlogBase(BaseModel):
    title: str
    excerpt: Optional[str]
    content: str

class BlogCreate(BlogBase):
    pass

class BlogUpdate(BlogBase):
    pass

class BlogResponse(BlogBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: datetime
    author_id: int
    full_name: str
    username: str

    class Config:
        from_attributes = True

class BlogWithoutBody(BaseModel):
    id: int
    slug: str
    title: str
    excerpt: str
    created_at: datetime
    updated_at: datetime
    author_id: int
    full_name: str
    username: str

class GetAllBlogsResponse(BaseModel):
    blogs: List[BlogWithoutBody]
    total_count: int

