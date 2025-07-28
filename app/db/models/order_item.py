import uuid

from sqlalchemy import DECIMAL, UUID, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

from decimal import Decimal


class OrderItem(Base):
    __tablename__ = "order_item"

    order_item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("order.order_id"), nullable=False
    )
    item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("item.item_id"), nullable=False
    )
    order_item_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    order_item_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    order = relationship("Order", back_populates="order_items")
    item = relationship("Item", back_populates="order_items")
