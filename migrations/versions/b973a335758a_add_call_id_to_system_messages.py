"""add call id to system messages

Revision ID: b973a335758a
Revises: a51bbf792854
Create Date: 2026-09-30 18:02:12.039934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b973a335758a'
down_revision = 'a51bbf792854'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("messages", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "call_id",
                sa.Integer(),
                nullable=True,
            )
        )
        batch_op.create_index(
            batch_op.f("ix_messages_call_id"),
            ["call_id"],
            unique=False,
        )
        batch_op.create_foreign_key(
            None,
            "calls",
            ["call_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade():
    with op.batch_alter_table("messages", schema=None) as batch_op:
        batch_op.drop_constraint(
            None,
            type_="foreignkey",
        )
        batch_op.drop_index(
            batch_op.f("ix_messages_call_id")
        )
        batch_op.drop_column("call_id")

    # ### end Alembic commands ###
