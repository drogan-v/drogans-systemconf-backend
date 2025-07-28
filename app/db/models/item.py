import uuid
from decimal import Decimal

from sqlalchemy import DECIMAL, UUID, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Item(Base):
    __tablename__ = "item"

    item_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    item_name: Mapped[str] = mapped_column(String(255), nullable=False)
    item_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    item_description: Mapped[str] = mapped_column(String(255), nullable=False)

    order_items = relationship("OrderItem", back_populates="item")
