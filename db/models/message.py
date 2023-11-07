from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship, backref

from db.models.base import BaseModel


class ChatEnum(Enum):
    POSTS = "POSTS"
    IMAGES = "IMAGES"
    THEMES = "THEMES"


class MessageTypeEnum(Enum):
    TEXT = "TEXT"
    POST = "POST"
    IMAGE = "IMAGE"
    THEME = "THEME"


class SenderEnum(Enum):
    USER = "USER"
    SYSTEM = "SYSTEM"


class Message(BaseModel):
    id = Column(Integer, primary_key=True)
    type = Column(ENUM(MessageTypeEnum))
    chat = Column(ENUM(ChatEnum))
    sender = Column(ENUM(SenderEnum))
    data = Column(String)
    datetime = Column(DateTime)
    post_id = Column(Integer, ForeignKey('post.id', ondelete='SET NULL'))
    post = relationship('Post', backref=backref('message', uselist=False))
    image_id = Column(Integer, ForeignKey('image.id', ondelete='SET NULL'))
    image = relationship('Image', backref=backref('message', uselist=False))
    project_id = Column(Integer, ForeignKey('project.id', ondelete='SET NULL'))
    project = relationship('Project', back_populates='messages')
