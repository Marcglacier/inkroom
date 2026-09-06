"""preserve messages from deleted users

Revision ID: ce0599fba1d5
Revises: 321c9695d6af
Create Date: 2026-08-13 16:22:12.136862

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce0599fba1d5'
down_revision = '321c9695d6af'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("messages", schema=None) as batch_op:
        batch_op.alter_column(
            "sender_id",
            existing_type=sa.INTEGER(),
            nullable=True,
        )
        batch_op.drop_constraint(
            batch_op.f("messages_sender_id_fkey"),
            type_="foreignkey",
        )
        batch_op.create_foreign_key(
            None,
            "users",
            ["sender_id"],
            ["id"],
            ondelete="SET NULL",
        )

def downgrade():
    with op.batch_alter_table("messages", schema=None) as batch_op:
        batch_op.drop_constraint(
            None,
            type_="foreignkey",
        )
        batch_op.create_foreign_key(
            batch_op.f("messages_sender_id_fkey"),
            "users",
            ["sender_id"],
            ["id"],
            ondelete="CASCADE",
        )
        batch_op.alter_column(
            "sender_id",
            existing_type=sa.INTEGER(),
            nullable=False,
        )