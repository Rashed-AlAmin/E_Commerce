import uuid
from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from backend.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
