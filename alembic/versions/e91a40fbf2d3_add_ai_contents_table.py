"""add ai_contents table

Revision ID: e91a40fbf2d3
Revises: 16655af813ee
Create Date: 2025-11-23 18:30:34.489869

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e91a40fbf2d3'
down_revision: Union[str, Sequence[str], None] = '16655af813ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: create ai_contents table."""
    op.create_table(
        "ai_contents",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column(
            "product_id",
            sa.Integer,
            sa.ForeignKey("products.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("channel", sa.String(length=50), nullable=False),
        sa.Column("content_type", sa.String(length=50), nullable=False),
        sa.Column(
            "payload",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "approved",
            sa.Boolean,
            nullable=False,
            server_default=sa.text("FALSE"),
        ),
        sa.Column("last_model_used", sa.String(length=100), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )

    op.create_index(
        "ix_ai_contents_product_channel_type",
        "ai_contents",
        ["product_id", "channel", "content_type"],
    )


def downgrade() -> None:
    """Downgrade schema: drop ai_contents table."""
    op.drop_index("ix_ai_contents_product_channel_type", table_name="ai_contents")
    op.drop_table("ai_contents")
