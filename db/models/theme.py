from sqlalchemy import Integer, Column, Text, ForeignKey
from sqlalchemy.orm import relationship

from db.models.base import BaseModel


class Theme(BaseModel):
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey('project.id', ondelete='SET NULL'))
    project = relationship('Project', back_populates='themes')
    post_type_id = Column(Integer, ForeignKey('posttype.id', ondelete='SET NULL'))
    post_type = relationship('PostType', back_populates='themes')
    posts = relationship('Post', back_populates='theme')
