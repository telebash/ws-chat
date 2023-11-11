from pydantic import BaseModel

from schemas.token import Token


class CreateTheme(Token):
    niche: str
    text_style: str
