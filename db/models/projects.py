from sqlalchemy import Column, Integer, String, Boolean, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

from db.models.base import BaseModel


class Projects(BaseModel):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    custom = Column(Boolean, default=False)

    themes = relationship('Themes', backref='project')
    user_id = Column(BigInteger, ForeignKey('user.id', ondelete='SET NULL'))
