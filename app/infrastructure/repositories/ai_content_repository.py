"""
AIContent repository.

Responsibilities:
- Encapsulate all database operations related to AIContent.
- Provide a clean API for the service layer.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.models.ai_content import AIContent
from app.domain.schemas.ai_content import AIContentCreate


def get_ai_content(db: Session, ai_content_id: int) -> Optional[AIContent]:
    """Return a single AIContent by ID, or None if not found."""
    return db.query(AIContent).filter(AIContent.id == ai_content_id).first()


def get_ai_contents_by_product(
    db: Session,
    product_id: int,
    channel: Optional[str] = None,
    content_type: Optional[str] = None,
) -> List[AIContent]:
    """
    Return AI contents for a given product, optionally filtered by channel and content_type.
    """
    query = db.query(AIContent).filter(AIContent.product_id == product_id)

    if channel:
        query = query.filter(AIContent.channel == channel)

    if content_type:
        query = query.filter(AIContent.content_type == content_type)

    # Newest first
    return query.order_by(AIContent.created_at.desc()).all()


def create_ai_content(db: Session, data: AIContentCreate) -> AIContent:
    """
    Create a new AIContent row from validated data.
    """
    ai_content = AIContent(
        product_id=data.product_id,
        channel=data.channel,
        content_type=data.content_type,
        payload=data.payload,
        approved=data.approved,
        last_model_used=data.last_model_used,
    )
    db.add(ai_content)
    db.commit()
    db.refresh(ai_content)
    return ai_content
