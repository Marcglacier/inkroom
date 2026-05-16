"""add counters to posts

Revision ID: 0e71142ae628
Revises: 545ff0d8c24f
Create Date: 2026-05-16 12:05:06.381788
"""

from alembic import op
import sqlalchemy as sa

revision = '0e71142ae628'
down_revision = '545ff0d8c24f'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('posts', schema=None) as batch_op:

        # 🔥 SAFE DEFAULTS FOR EXISTING ROWS
        batch_op.add_column(
            sa.Column(
                'comments_count',
                sa.Integer(),
                nullable=False,
                server_default='0'
            )
        )

        batch_op.add_column(
            sa.Column(
                'reposts_count',
                sa.Integer(),
                nullable=False,
                server_default='0'
            )
        )

    # optional cleanup (keeps schema clean after migration)
    op.execute("UPDATE posts SET comments_count = 0 WHERE comments_count IS NULL")
    op.execute("UPDATE posts SET reposts_count = 0 WHERE reposts_count IS NULL")


def downgrade():
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.drop_column('reposts_count')
        batch_op.drop_column('comments_count')