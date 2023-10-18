from pydantic import BaseModel


class CreateTheme(BaseModel):
    project: str
    text_style: str
