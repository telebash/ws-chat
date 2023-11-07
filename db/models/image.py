from sqlalchemy import Boolean, Column, Integer, Text, ForeignKey, BigInteger, String
from sqlalchemy.orm import relationship

from db.models.base import BaseModel, TimestampModel


class Image(BaseModel, TimestampModel):
    id = Column(Integer, primary_key=True)
    like = Column(Boolean, default=False)
    dislike = Column(Boolean, default=False)
    url = Column(String, nullable=False)
    style = Column(String, nullable=False)
    seed = Column(BigInteger)
    prompt = Column(Text)

    # project_id = Column(Integer, ForeignKey('project.id', ondelete='SET NULL'))
    # project = relationship('Project', back_populates='images')
