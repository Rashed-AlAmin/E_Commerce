import uuid
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from backend.db.base import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cart_id = Column(UUID(as_uuid=True), ForeignKey("carts.id"))
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"))
    quantity = Column(Integer, default=1)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")
