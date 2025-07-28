from sqlalchemy import Column, String, UUID, DECIMAL

from app.db.session import Base
from sqlalchemy.orm import relationship
import uuid

class Item(Base):
    __tablename__ = "item"

    item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_name = Column(String(255), nullable=False)
    item_price = Column(DECIMAL(10, 2), nullable=False)
    item_description = Column(String(255), nullable=True)

    order_items = relationship("OrderItem", back_populates="item")