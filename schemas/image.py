from pydantic import BaseModel


class CreateImage(BaseModel):
    text: str
    style: str
    scale_data: str


class UpscaleImage(BaseModel):
    image_name: str
    scale_data: str
