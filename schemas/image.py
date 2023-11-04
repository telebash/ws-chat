from pydantic import BaseModel

from schemas.token import Token


class CreateImage(Token):
    text: str
    style: str
    scale_data: str


class UpscaleImage(Token):
    image_name: str
    scale_data: str
