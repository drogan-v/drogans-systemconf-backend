from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import declarative_base, relationship
import uuid

Base = declarative_base()


class ShippingAddress(Base):
    __tablename__ = 'shipping_address'

    shipping_address_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_code = Column(String(2), nullable=False)
    state = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    street_line1 = Column(String(255), nullable=False)
    street_line2 = Column(String(255), nullable=False)
    post_code = Column(String(255), nullable=False)

    order_info = relationship("OrderInfo", back_populates="shipping_address", uselist=False)
