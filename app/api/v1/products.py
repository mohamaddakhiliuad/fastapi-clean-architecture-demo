"""
Products API Router.

Responsibilities now (with Service Layer):
- Define HTTP endpoints for Product CRUD operations.
- Call ProductService for all business logic.
- Return clean Pydantic schemas to API clients.
"""


from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.infrastructure.db.session import get_db
from app.domain.schemas.product import ProductRead, ProductCreate, ProductUpdate

from app.domain.schemas.ai_content import AIContentRead
from app.domain.services.product_service import ProductService



router = APIRouter(
    prefix="/products",
    tags=["products"],
)


@router.get("/", response_model=List[ProductRead])
def list_products(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """
    Return a paginated list of products using ProductService.
    """
    return ProductService.list_products(db=db, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductRead)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
):
    """
    Return a single product by ID.
    Raises 404 if product does not exist.
    """
    return ProductService.get_product(db=db, product_id=product_id)


@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product_endpoint(
    payload: ProductCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new product and return it using ProductService.
    """
    return ProductService.create_product(db=db, data=payload)


@router.put("/{product_id}", response_model=ProductRead)
def update_product_endpoint(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
):
    """
    Update an existing product.
    Raises 404 if product does not exist.
    """
    return ProductService.update_product(
        db=db,
        product_id=product_id,
        data=payload,
    )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_endpoint(
    product_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete an existing product.
    Raises 404 if product does not exist.s          
    """
    ProductService.delete_product(db=db, product_id=product_id)
    return None




@router.get(
    "/{product_id}/ai-contents",
    response_model=List[AIContentRead],
    summary="List AI-generated contents for a product",
)
def list_ai_contents_for_product(
    product_id: int,
    channel: Optional[str] = None,
    content_type: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Return AI-generated contents for the specified product.

    Optional filters:
    - channel: 'ebay', 'shopify', 'instagram', ...
    - content_type: 'title', 'description', 'full_listing', 'caption', ...
    """
    return ProductService.list_ai_contents_for_product(
        db=db,
        product_id=product_id,
        channel=channel,
        content_type=content_type,
    )
@router.post(
    "/{product_id}/generate/ebay",
    response_model=AIContentRead,
    summary="Generate an eBay listing for a product using AI",
)
def generate_ebay_listing_for_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    """
    Generate an eBay listing (demo implementation) for the given product.

    This will:
    - Call ProductService.generate_ebay_listing
    - Store the result in `ai_contents`
    - Return the created AIContent row
    """
    return ProductService.generate_ebay_listing(db=db, product_id=product_id)
