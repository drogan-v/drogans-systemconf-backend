from sqlalchemy import Column, ForeignKey, UUID, DECIMAL, Integer
from sqlalchemy.orm import relationship
from app.db.session import Base
import uuid

class OrderItem(Base):
    __tablename__ = "order_item"

    order_item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("order.order_id"), nullable=False)
    item_id = Column(UUID(as_uuid=True), ForeignKey("item.item_id"), nullable=False)
    order_item_quantity = Column(Integer, nullable=False)
    order_item_price = Column(DECIMAL(10, 2), nullable=False)

    order = relationship("Order", back_populates="order_items")
    item = relationship("Item", back_populates="order_items")