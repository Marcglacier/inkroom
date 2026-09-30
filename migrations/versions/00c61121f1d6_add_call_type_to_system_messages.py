"""add call type to system messages

Revision ID: 00c61121f1d6
Revises: b973a335758a
Create Date: 2026-09-30 20:05:11.092550

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '00c61121f1d6'
down_revision = 'b973a335758a'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'call_type',
                sa.String(length=20),
                nullable=True,
            )
        )


def downgrade():
    with op.batch_alter_table('messages', schema=None) as batch_op:
        batch_op.drop_column('call_type')