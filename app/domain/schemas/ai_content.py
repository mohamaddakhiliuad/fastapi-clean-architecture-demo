from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class AIContentBase(BaseModel):
    """
    Base schema for AIContent shared fields.
    """
    product_id: int = Field(..., description="ID of the product this AI content belongs to.")
    channel: str = Field(..., description="Target channel, e.g. 'ebay', 'shopify', 'instagram'.")
    content_type: str = Field(
        ...,
        description="Type of AI content, e.g. 'title', 'description', 'full_listing', 'caption'.",
    )
    payload: Dict[str, Any] = Field(
        ..., description="Flexible JSON payload containing the AI-generated content."
    )
    approved: bool = Field(False, description="Whether this AI content is approved by a human.")
    last_model_used: Optional[str] = Field(
        None,
        description="Name of the AI model that generated this content.",
    )


class AIContentCreate(AIContentBase):
    """
    Schema used when creating a new AIContent entry.
    """
    pass


class AIContentRead(AIContentBase):
    """
    Schema used when returning AIContent to the client.
    """
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # for SQLAlchemy model compatibility
