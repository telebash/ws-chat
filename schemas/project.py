from typing import Optional

from pydantic import BaseModel

from schemas.token import Token


class ProjectBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class ProjectCreate(ProjectBase, Token):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
