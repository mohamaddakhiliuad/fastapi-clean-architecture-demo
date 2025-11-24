
"""create ai_contents table real

Revision ID: abcd1234create
Revises: e91a40fbf2d3
Create Date: 2025-11-23 20:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '649ce434e5bf' # همونی که بالا تو فایل خودت هست
down_revision: Union[str, Sequence[str], None] = "e91a40fbf2d3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: create ai_contents table."""
    op.create_table(
        "ai_contents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("product_id", sa.Integer(), nullable=False),
        sa.Column("channel", sa.String(length=50), nullable=False),
        sa.Column("content_type", sa.String(length=50), nullable=False),
        sa.Column(
            "payload",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column(
            "approved",
            sa.Boolean(),
            server_default=sa.text("FALSE"),
            nullable=False,
        ),
        sa.Column("last_model_used", sa.String(length=100), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_ai_contents_product_channel_type"),
        "ai_contents",
        ["product_id", "channel", "content_type"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema: drop ai_contents table."""
    op.drop_index(
        op.f("ix_ai_contents_product_channel_type"),
        table_name="ai_contents",
    )
    op.drop_table("ai_contents")
