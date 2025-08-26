from sqlalchemy import Column, Integer, String, Text
from .base import Base

class PaymentRequest(Base):
    __tablename__ = "payment_requests"
    id = Column(Integer, primary_key=True)
    hash = Column(String(64), unique=True, nullable=False, index=True)
    amount_minor = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(32), default="created", index=True)
    stripe_session_id = Column(String(128), nullable=True, index=True)
