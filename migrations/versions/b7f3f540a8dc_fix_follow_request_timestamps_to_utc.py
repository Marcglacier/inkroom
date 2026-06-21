"""fix follow_request timestamps to UTC

Revision ID: b7f3f540a8dc
Revises: d9ff3cbafe50
Create Date: 2026-06-10 16:03:54.888139
"""

from alembic import op
import sqlalchemy as sa
from datetime import timezone

# --- Alembic identifiers ---
revision = "b7f3f540a8dc"
down_revision = "d9ff3cbafe50"
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()

    # 1. Fix existing rows FIRST (important)
    result = connection.execute(
        sa.text("SELECT id, created_at FROM follow_requests")
    )

    for row in result:
        if row.created_at is None:
            continue

        # only fix naive timestamps
        if row.created_at.tzinfo is None:
            fixed = row.created_at.replace(tzinfo=timezone.utc)

            connection.execute(
                sa.text("""
                    UPDATE follow_requests
                    SET created_at = :fixed
                    WHERE id = :id
                """),
                {"fixed": fixed, "id": row.id}
            )

    # 2. Then alter column type safely
    with op.batch_alter_table("follow_requests") as batch_op:
        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(),  # important: match current reality
            type_=sa.DateTime(timezone=True),
            nullable=False,
        )


def downgrade():
    with op.batch_alter_table("follow_requests") as batch_op:
        batch_op.alter_column(
            "created_at",
            type_=sa.DateTime(),
            nullable=True,
        )
