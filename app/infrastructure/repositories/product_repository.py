"""
Product repository.

Responsibilities:
- Encapsulate all database operations related to Product.
- Provide a clean API for the service / API layers.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.models.product import Product
from app.domain.schemas.product import ProductCreate, ProductUpdate


def get_product(db: Session, product_id: int) -> Optional[Product]:
    """Return a single product by ID, or None if not found."""
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 50) -> List[Product]:
    """Return a list of products with pagination."""
    return (
        db.query(Product)
        .order_by(Product.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_product(db: Session, data: ProductCreate) -> Product:
    """Create and persist a new product."""
    product = Product(
        name=data.name,
        sku=data.sku,
        price=data.price,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(
    db: Session, product: Product, data: ProductUpdate
) -> Product:
    """Update an existing product with provided fields."""
    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product) -> None:
    """Delete an existing product."""
    db.delete(product)
    db.commit()
