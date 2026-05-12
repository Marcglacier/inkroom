"""add conversation participants

Revision ID: 6a44861b7f1c
Revises: 30f96a00ee7a
Create Date: 2026-05-12 17:10:54.384135
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6a44861b7f1c"
down_revision = "30f96a00ee7a"
branch_labels = None
depends_on = None


def upgrade():
    # Add columns as nullable to avoid errors with existing rows
    with op.batch_alter_table("conversations", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user1_id", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("user2_id", sa.Integer(), nullable=True))

        batch_op.create_foreign_key(
            "fk_conversations_user1",
            "users",
            ["user1_id"],
            ["id"],
        )

        batch_op.create_foreign_key(
            "fk_conversations_user2",
            "users",
            ["user2_id"],
            ["id"],
        )


def downgrade():
    with op.batch_alter_table("conversations", schema=None) as batch_op:
        batch_op.drop_constraint("fk_conversations_user2", type_="foreignkey")
        batch_op.drop_constraint("fk_conversations_user1", type_="foreignkey")

        batch_op.drop_column("user2_id")
        batch_op.drop_column("user1_id")