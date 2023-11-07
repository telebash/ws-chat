from sqlalchemy import Boolean, Column, Integer, Text, ForeignKey, String
from sqlalchemy.orm import relationship

from db.models.base import BaseModel, TimestampModel


class PostType(BaseModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    # themes = relationship('Theme', back_populates='post_type')


class Post(BaseModel, TimestampModel):
    id = Column(Integer, primary_key=True)
    like = Column(Boolean, default=False)
    dislike = Column(Boolean, default=False)
    text = Column(Text, nullable=False)
    theme_text = Column(Text)
    # theme_id = Column(Integer, ForeignKey('theme.id', ondelete='SET NULL'))
    # theme = relationship('Theme', back_populates='posts')
    # project_id = Column(Integer, ForeignKey('project.id', ondelete='SET NULL'))
    # project = relationship('Project', back_populates='posts')
