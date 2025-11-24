from sqlalchemy import Column, Integer, String, Numeric, Boolean
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship

from app.infrastructure.db.session import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    sku = Column(String(100), nullable=True, unique=True)
    price = Column(Numeric(10, 2), nullable=True)
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
  # New relationship to AIContent
    ai_contents = relationship(
        "AIContent",
        back_populates="product",
        cascade="all, delete-orphan",
    )