"""enforce non-null forwarded message flag

Revision ID: 461d222d889d
Revises: e7fd04fb931d
"""
from alembic import op
import sqlalchemy as sa


revision = "461d222d889d"
down_revision = "e7fd04fb931d"
branch_labels = None
depends_on = None


def upgrade():
    # Existing NULL values mean the message was not marked as forwarded.
    op.execute(
        sa.text(
            "UPDATE messages "
            "SET is_forwarded = FALSE "
            "WHERE is_forwarded IS NULL"
        )
    )

    op.alter_column(
        "messages",
        "is_forwarded",
        existing_type=sa.Boolean(),
        nullable=False,
        server_default=sa.text("FALSE"),
    )


def downgrade():
    op.alter_column(
        "messages",
        "is_forwarded",
        existing_type=sa.Boolean(),
        nullable=True,
        server_default=None,
    )
