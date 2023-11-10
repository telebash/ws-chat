import datetime

from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from db.models.base import BaseModel, TimestampModel


class User(BaseModel, TimestampModel):
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    projects = relationship("Project", back_populates="user")
    paid = Column(Boolean, default=False)
    subscription_date = Column(DateTime)
    payments = relationship("Payment", back_populates="user", order_by="Payment.created_at.desc()")
    # free_use = Column(Integer, default=5)
    # free_use_bool = Column(Boolean, default=True)
    # plus_3_days = Column(Boolean, default=False)
    # promo_code = relationship("PromoCode", back_populates="user", uselist=False)
    #

    def __str__(self):
        return str(self.username)
    
    async def update(
        self,
        session: AsyncSession,
        free_use: str = None,
        free_use_bool: str = None,
        paid: bool = None,
        paid_date: datetime.datetime = None,
    ) -> None:
        if paid is not None:
            self.paid = paid
        if paid_date is not None:
            self.subscription_date = paid_date
        await session.commit()
    #
    # @property
    # def is_admin_user(self):
    #     return self.username in [
    #         'zephyr_er', 'X3gxu', 'Nowayanna', 'murza_design',
    #         'Rocky_Raccoon', 'Asselie', 'rasult22js', 'abaibolsai',
    #         'alimzhan'
    #     ]
