from pydantic import BaseModel


class CreatePost(BaseModel):
    theme: str
    project: str
    text_style: str
