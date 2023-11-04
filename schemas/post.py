from typing import Optional

from pydantic import BaseModel

from schemas.token import Token


class PostBase(BaseModel):
    theme: Optional[str] = None
    project: Optional[str] = None
    text_style: Optional[str] = None


class PostCreate(Token):
    theme: str
    project: str
    text_style: str


class PostUpdate(PostBase):
    pass


class PostInDBBase(PostBase):
    id: int
    created_at: str
    updated_at: str

