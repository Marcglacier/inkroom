"""add viewed fields to message media

Revision ID: 6d9846c4b0b1
Revises: 06d1db796132
Create Date: 2026-07-02 11:44:29.455771

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6d9846c4b0b1"
down_revision = "06d1db796132"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("message_media", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "viewed",
                sa.Boolean(),
                nullable=False,
                server_default=sa.false(),
            )
        )

        batch_op.add_column(
            sa.Column(
                "viewed_at",
                sa.DateTime(),
                nullable=True,
            )
        )

    # Remove the server default after existing rows are updated
    op.alter_column(
        "message_media",
        "viewed",
        server_default=None,
    )


def downgrade():
    with op.batch_alter_table("message_media", schema=None) as batch_op:
        batch_op.drop_column("viewed_at")
        batch_op.drop_column("viewed")