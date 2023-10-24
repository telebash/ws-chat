from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    theme: Optional[str] = None
    project: Optional[str] = None
    text_style: Optional[str] = None


class PostCreate(PostBase):
    theme: str
    project: str
    text_style: str


class PostUpdate(PostBase):
    pass


class PostInDBBase(PostBase):
    id: int
    created_at: str
    updated_at: str

