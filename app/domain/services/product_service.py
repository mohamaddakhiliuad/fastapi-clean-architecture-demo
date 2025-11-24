
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status



from app.domain.schemas.product import ProductCreate, ProductUpdate, ProductRead
from app.infrastructure.repositories import product_repository


from app.domain.schemas.ai_content import AIContentRead, AIContentCreate
from app.infrastructure.repositories import ai_content_repository
"""
ProductService

Service Layer for the Product domain.

Responsibilities:
- Encapsulates all business logic related to Product operations.
- Acts as the orchestrator between API routers, domain schemas, and repository layer.
- Validates business rules before persisting or updating data.
- Raises HTTP exceptions for API-friendly error handling.
- Converts input DTOs (ProductCreate, ProductUpdate) into repository calls.
- Returns output DTOs (ProductRead) back to the API layer.

Architecture Notes (Project Standard):
- Schemas (Pydantic) enforce input/output validation.
- Repository handles all DB operations (SQLAlchemy).
- Service layer MUST NOT contain database queries directly.
- Service functions remain stateless and pure where possible.
- Exceptions are raised here, not in the repository, to keep repositories clean and logic-free.
"""

class ProductService:
    """
    Service layer for Product.
    مسئول منطق بیزنسی + صدا زدن Repository.
    """

    @staticmethod
    def list_products(
        db: Session,
        skip: int = 0,
        limit: int = 50,
    ) -> List[ProductRead]:
        products = product_repository.get_products(db=db, skip=skip, limit=limit)
        return products

    @staticmethod
    def get_product(
        db: Session,
        product_id: int,
    ) -> ProductRead:
        product = product_repository.get_product(db=db, product_id=product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )
        return product

    @staticmethod
    def create_product(
        db: Session,
        data: ProductCreate,
    ) -> ProductRead:
        product = product_repository.create_product(db=db, data=data)
        return product

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        data: ProductUpdate,
    ) -> ProductRead:
        product = product_repository.get_product(db=db, product_id=product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        updated = product_repository.update_product(db=db, product=product, data=data)
        return updated

    @staticmethod
    def delete_product(
        db: Session,
        product_id: int,
    ) -> None:
        product = product_repository.get_product(db=db, product_id=product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        product_repository.delete_product(db=db, product=product)
        # برنمی‌گردونیم چیزی؛ Router می‌تونه status 204 بده
        return None
    @staticmethod
    def list_ai_contents_for_product(
        db: Session,
        product_id: int,
        channel: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> List[AIContentRead]:
        """
        Return AI-generated contents for a given product, optionally filtered by channel/content_type.
        """
        # Ensure the product exists (re-use the existing get_product logic)
        product = product_repository.get_product(db=db, product_id=product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        ai_contents = ai_content_repository.get_ai_contents_by_product(
            db=db,
            product_id=product_id,
            channel=channel,
            content_type=content_type,
        )

        # FastAPI / Pydantic will handle conversion to AIContentRead via response_model
        return ai_contents
    @staticmethod
    def generate_ebay_listing(
        db: Session,
        product_id: int,
        model_name: str = "gpt-5.1",
    ) -> AIContentRead:
        """
        Generate an eBay listing for a given product using AI and store it in ai_contents.

        Steps:
        - Load product from DB.
        - Build prompt from product fields.
        - Call AI model (OpenAI).
        - Store result in ai_contents.
        - Return created AIContent.
        """
        product = product_repository.get_product(db=db, product_id=product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found.",
            )

        # TODO: build prompt from product UPM data
        # prompt = build_ebay_prompt(product)

        # TODO: call OpenAI and get structured payload
        # ai_result_payload = call_openai_for_ebay(prompt, model_name=model_name)

        # Temporary placeholder payload (until AI integration is wired)
        ai_result_payload = {
            "title": f"[DEMO] eBay title for product #{product.id}",
            "subtitle": "Demo subtitle generated by AI.",
            "description_html": "<p>This is a demo eBay listing description.</p>",
            "seo_keywords": ["demo", "ebay", "ai"],
        }

        ai_content_create = AIContentCreate(
            product_id=product.id,
            channel="ebay",
            content_type="full_listing",
            payload=ai_result_payload,
            approved=False,
            last_model_used=model_name,
        )

        ai_content = ai_content_repository.create_ai_content(db=db, data=ai_content_create)
        return ai_content
