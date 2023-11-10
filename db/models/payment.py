from pydantic import BaseModel
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func
)
from sqlalchemy.orm import relationship

from db.models.base import TimestampModel


class Payment(BaseModel, TimestampModel):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    currency = Column(String, nullable=False)
    total_amount = Column(Integer, nullable=False)
    invoice_payload = Column(String)
    provider_payment_charge_id = Column(String)
    date = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="payments")

    @property
    def type_of_payment(self):
        if self.total_amount == 200000:
            return "DAY"
        elif self.total_amount == 1000000:
            return "WEEK"
        elif self.total_amount == 2000000:
            return "MONTH"
