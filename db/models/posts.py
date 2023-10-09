from sqlalchemy import Boolean, Column, Integer, Text, ForeignKey, BigInteger, String
from sqlalchemy.orm import relationship

from db.models.base import BaseModel, TimestampModel


class Post(BaseModel, TimestampModel):
    like = Column(Boolean, default=False)
    dislike = Column(Boolean, default=False)
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    theme_id = Column(Integer, ForeignKey('themes.id', ondelete='SET NULL'))
    theme_text = Column(Text)
    message_id = Column(Integer)
    telegram_id = Column(BigInteger, ForeignKey('user.telegram_id', ondelete='SET NULL'))
    user = relationship('User', backref='user_post')


class PostImage(BaseModel, TimestampModel):
    id = Column(Integer, primary_key=True)
    like = Column(Boolean, default=False)
    dislike = Column(Boolean, default=False)
    message_id = Column(Integer)
    url = Column(String, nullable=False)
    style = Column(String, nullable=False)
    seed = Column(BigInteger)
    prompt = Column(Text)

    telegram_id = Column(BigInteger, ForeignKey('user.telegram_id', ondelete='SET NULL'))
    user = relationship('User', backref='user_post_image')
