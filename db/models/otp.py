from enum import Enum

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from db.models.base import BaseModel


class OtpTypeEnum(Enum):
    FORGOT_PASSWORD = 'FORGOT_PASSWORD'
    VERIFY_EMAIL = 'VERIFY_EMAIL'


class Otp(BaseModel):
    id = Column(Integer, primary_key=True)
    code = Column(String(6), nullable=False, unique=True)
    type = Column(ENUM(OtpTypeEnum))
    user_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL'))
    user = relationship('User', back_populates='otps')
