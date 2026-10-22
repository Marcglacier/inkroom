
"""add user blocks

Revision ID: e7fd04fb931d
Revises: 62b3c5416022
"""
from alembic import op
import sqlalchemy as sa


revision = "e7fd04fb931d"
down_revision = "62b3c5416022"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_blocks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("blocker_id", sa.Integer(), nullable=False),
        sa.Column("blocked_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "blocker_id != blocked_id",
            name="ck_user_block_not_self",
        ),
        sa.ForeignKeyConstraint(
            ["blocked_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["blocker_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "blocker_id",
            "blocked_id",
            name="uq_user_block_pair",
        ),
    )

    op.create_index(
        "idx_user_block_blocked",
        "user_blocks",
        ["blocked_id"],
        unique=False,
    )
    op.create_index(
        "idx_user_block_blocker",
        "user_blocks",
        ["blocker_id"],
        unique=False,
    )


def downgrade():
    op.drop_index("idx_user_block_blocker", table_name="user_blocks")
    op.drop_index("idx_user_block_blocked", table_name="user_blocks")
    op.drop_table("user_blocks")
