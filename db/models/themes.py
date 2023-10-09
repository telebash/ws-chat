from sqlalchemy import Integer, Column, Text, ForeignKey
from sqlalchemy.orm import relationship

from db.models.base import BaseModel


class Themes(BaseModel):
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    niche_id = Column(Integer, ForeignKey('niches.id', ondelete='SET NULL'))
    post_type_id = Column(Integer, ForeignKey('posttypes.id', ondelete='SET NULL'))

    posts = relationship('Post', backref='theme')
