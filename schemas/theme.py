from pydantic import BaseModel

from schemas.token import Token


class CreateTheme(Token):
    project: str
    text_style: str
