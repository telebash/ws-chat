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
    chat: ChatEnum
    sender: SenderEnum
    data: str
    datetime: python_datetime
    project_id: int

    class Config:
        orm_mode = True


class SaveMessage(SaveMessageBase, Token):
    pass


class SaveMessages(Token):
    messages: list[SaveMessageBase]
