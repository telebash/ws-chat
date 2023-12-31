from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.models.base import BaseModel, TimestampModel


class Project(BaseModel, TimestampModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True, default=None)
    niche = Column(String(255), nullable=False)
    is_favourite = Column(Boolean, default=False)
    image_url = Column(String(255), nullable=True, default=None)
    # themes = relationship('Theme', back_populates='project')
    # images = relationship('Image', back_populates='project')
    # posts = relationship('Post', back_populates='project')
    messages = relationship('Message', back_populates='project')
    user_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL'))
    user = relationship('User', back_populates='projects')
