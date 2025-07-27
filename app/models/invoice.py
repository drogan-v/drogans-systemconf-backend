from sqlalchemy import Column, ForeignKey, String, Integer, BigInteger
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Invoice(Base):
    __tablename__ = 'invoice'

    invoice_id = Column(String(255), primary_key=True)
    from_user_id = Column(BigInteger, ForeignKey("user.user_id"), nullable=False)
    currency = Column(String(3), nullable=False)
    total_amount = Column(Integer, nullable=False)
    invoice_payload = Column(String(255), nullable=False)

    from_user = relationship("User", back_populates="invoices")
