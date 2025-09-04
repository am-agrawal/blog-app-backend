from pydantic import BaseModel
from typing import Optional
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
    author_id: int
    author_name: str

    class Config:
        from_attributes = True
