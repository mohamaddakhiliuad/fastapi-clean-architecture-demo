from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.infrastructure.db.session import Base


class AIContent(Base):
    """
    AI-generated content attached to a Product.

    Each row represents one AI result for a specific:
    - product (product_id)
    - channel (ebay, shopify, instagram, ...)
    - content_type (title, description, full_listing, caption, ...)

    Payload is stored as JSONB so it is flexible for different use cases.
    """

    __tablename__ = "ai_contents"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    channel = Column(String(50), nullable=False)  # e.g. 'ebay', 'shopify', 'instagram'
    content_type = Column(
        String(50), nullable=False
    )  # e.g. 'title', 'description', 'full_listing', 'caption'

    payload = Column(
        JSONB(astext_type=Text),
        nullable=False,
        doc="Raw AI output as JSON (title/body/hashtags/...)",
    )

    approved = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
        doc="Indicates whether a human has approved this AI content.",
    )
    last_model_used = Column(
        String(100),
        nullable=True,
        doc="Name of the model that generated this content, e.g. 'gpt-5.1'.",
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        doc="Timestamp when the AI content was created.",
    )

    # Relationship back to Product (assuming Product model has ai_contents relationship)
    product = relationship(
        "Product",
        back_populates="ai_contents",
    )
