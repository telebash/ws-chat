from typing import Optional
from datetime import datetime as python_datetime

from pydantic import BaseModel

from schemas.token import Token
from services import ChatEnum, MessageTypeEnum, SenderEnum


class GetMessages(Token):
    project_id: int
    chat: ChatEnum
    skip: Optional[int] = 0
    limit: Optional[int] = 100


class SaveMessageBase(BaseModel):
    type: MessageTypeEnum
    sender: SenderEnum
    data: str
    datetime: python_datetime
    post_id: Optional[int] = None
    image_id: Optional[int] = None

    class Config:
        orm_mode = True


class SaveMessage(SaveMessageBase):
    chat: ChatEnum
    project_id: int


class SaveMessages(BaseModel):
    messages: list[SaveMessageBase]
    chat: ChatEnum
    project_id: int
