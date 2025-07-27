from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class User(Base):
    __tablename__ = 'user'

    user_id = Column(BigInteger, primary_key=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    username = Column(String(255), nullable=True)

    orders = relationship("Order", back_populates="user")
    invoices = relationship("Invoice", back_populates="from_user")
