"""
Pydantic schemas for Product.

Responsibilities:
- Define request/response shapes for Product API.
- Separate API layer from the SQLAlchemy model.
"""

from typing import Optional
from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Fields that are shared between read and write operations."""
    name: str = Field(..., min_length=1, max_length=255)
    sku: Optional[str] = Field(None, max_length=100)
    price: Optional[Decimal] = Field(None, ge=0)


class ProductCreate(ProductBase):
    """Schema for creating a new product."""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating an existing product."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    sku: Optional[str] = Field(None, max_length=100)
    price: Optional[Decimal] = Field(None, ge=0)
    is_active: Optional[bool] = None


class ProductRead(ProductBase):
    """Schema returned to clients when reading a product."""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # allows reading from SQLAlchemy models
