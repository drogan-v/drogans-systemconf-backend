from sqlalchemy import Column, ForeignKey, UUID, BigInteger, TIMESTAMP, func
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid


class Order(Base):
    __tablename__ = 'order'

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(BigInteger, ForeignKey('user.user_id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())

    user = relationship("User")
    order_items = relationship("OrderItem", back_populates="order")