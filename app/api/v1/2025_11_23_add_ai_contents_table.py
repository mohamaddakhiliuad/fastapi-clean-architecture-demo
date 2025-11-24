"""add ai_contents table

Revision ID: 20251123_add_ai_contents
Revises: <PUT_PREVIOUS_REVISION_ID_HERE>
Create Date: 2025-11-23

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "20251123_add_ai_contents"
down_revision = "<PUT_PREVIOUS_REVISION_ID_HERE>"
branch_labels = None
depends_on = None


def upgrade() -> None:
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
            postgresql.JSONB(astext_type=sa.Text()),  # requires Postgres
            nullable=False,
        ),
        sa.Column("approved", sa.Boolean, nullable=False, server_default=sa.text("FALSE")),
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
    op.drop_index("ix_ai_contents_product_channel_type", table_name="ai_contents")
    op.drop_table("ai_contents")
