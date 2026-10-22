"""add presence visibility preference

Revision ID: 459cf6c30043
Revises: 00c61121f1d6
"""

from alembic import op
import sqlalchemy as sa

revision = "459cf6c30043"
down_revision = "00c61121f1d6"
branch_labels = None
depends_on = None


def upgrade():
    # Add temporarily nullable so existing users can be backfilled.
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column(
                "show_online_status",
                sa.Boolean(),
                nullable=True,
            )
        )

    # Preserve existing visibility behaviour for all existing users.
    op.execute(
        "UPDATE users "
        "SET show_online_status = TRUE "
        "WHERE show_online_status IS NULL"
    )

    # Enforce a value for all future rows.
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "show_online_status",
            existing_type=sa.Boolean(),
            nullable=False,
        )


def downgrade():
    with op.batch_alter_table("users") as batch_op:
        batch_op.drop_column("show_online_status")