from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class OrderInfo(Base):
    __tablename__ = 'order_info'

    order_info_id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=True)
    phone_number = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    shipping_address_id = Column(UUID(as_uuid=True), ForeignKey("shipping_address.shipping_address_id"), nullable=True)

    shipping_address = relationship("ShippingAddress", back_populates="order_info")
    invoice = relationship("Invoice", back_populates="order_info", uselist=False)
