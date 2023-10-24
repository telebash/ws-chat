from typing import Optional

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class ProjectCreate(ProjectBase):
    name: str
    description: Optional[str] = None
    image_base64: Optional[str] = None
