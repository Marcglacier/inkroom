
"""add read receipts preference

Revision ID: 2dd9a6fa0d57
Revises: 459cf6c30043
"""

from alembic import op
import sqlalchemy as sa

revision = "2dd9a6fa0d57"
down_revision = "459cf6c30043"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "show_read_receipts",
                sa.Boolean(),
                server_default=sa.true(),
                nullable=False,
            )
        )
        # Existing users receive True; future changes are managed by the app.
        batch_op.alter_column(
            "show_read_receipts",
            existing_type=sa.Boolean(),
            server_default=None,
        )


def downgrade():
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_column("show_read_receipts")
