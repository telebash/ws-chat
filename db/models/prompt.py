from sqlalchemy import Column, Integer, Text

from db.models.base import BaseModel


class Prompts(BaseModel):
    id = Column(Integer, primary_key=True)
    prompt = Column(Text, nullable=False)
