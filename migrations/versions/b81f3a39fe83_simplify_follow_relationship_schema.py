"""simplify follow relationship schema

Revision ID: b81f3a39fe83
Revises: 5a52f7d5ac36
Create Date: 2026-08-15 14:33:58.988424

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "b81f3a39fe83"
down_revision = "5a52f7d5ac36"
branch_labels = None
depends_on = None


def upgrade():
    # ---------------------------------------------------------
    # FOLLOW REQUESTS
    # ---------------------------------------------------------
    with op.batch_alter_table("follow_requests", schema=None) as batch_op:

        # Prevent duplicate pending requests between the same users.
        batch_op.create_unique_constraint(
            "unique_follow_request",
            ["requester_id", "target_id"],
        )

        # Fast lookup by requester / target.
        batch_op.create_index(
            "idx_follow_request_requester",
            ["requester_id"],
            unique=False,
        )

        batch_op.create_index(
            "idx_follow_request_target",
            ["target_id"],
            unique=False,
        )

        # Requests should disappear automatically when a user is deleted.
        batch_op.drop_constraint(
            batch_op.f("follow_requests_target_id_fkey"),
            type_="foreignkey",
        )

        batch_op.drop_constraint(
            batch_op.f("follow_requests_requester_id_fkey"),
            type_="foreignkey",
        )

        batch_op.create_foreign_key(
            "fk_follow_requests_requester_user",
            "users",
            ["requester_id"],
            ["id"],
            ondelete="CASCADE",
        )

        batch_op.create_foreign_key(
            "fk_follow_requests_target_user",
            "users",
            ["target_id"],
            ["id"],
            ondelete="CASCADE",
        )

        # A row existing in this table now means:
        # "there is a pending follow request."
        batch_op.drop_column("status")

    # ---------------------------------------------------------
    # FOLLOWS
    # ---------------------------------------------------------
    with op.batch_alter_table("follows", schema=None) as batch_op:

        # A follow row itself is the source of truth.
        # No status column is needed.
        batch_op.drop_column("status")

        # Store follow creation time consistently as timezone-aware UTC.
        batch_op.alter_column(
            "created_at",
            existing_type=postgresql.TIMESTAMP(),
            type_=sa.DateTime(timezone=True),
            nullable=False,
        )


def downgrade():
    # ---------------------------------------------------------
    # FOLLOWS
    # ---------------------------------------------------------
    with op.batch_alter_table("follows", schema=None) as batch_op:

        batch_op.add_column(
            sa.Column(
                "status",
                sa.VARCHAR(length=20),
                nullable=False,
                server_default="following",
            )
        )

        batch_op.alter_column(
            "created_at",
            existing_type=sa.DateTime(timezone=True),
            type_=postgresql.TIMESTAMP(),
            nullable=True,
        )

    # ---------------------------------------------------------
    # FOLLOW REQUESTS
    # ---------------------------------------------------------
    with op.batch_alter_table("follow_requests", schema=None) as batch_op:

        batch_op.add_column(
            sa.Column(
                "status",
                sa.VARCHAR(length=20),
                nullable=True,
                server_default="pending",
            )
        )

        batch_op.drop_constraint(
            "fk_follow_requests_target_user",
            type_="foreignkey",
        )

        batch_op.drop_constraint(
            "fk_follow_requests_requester_user",
            type_="foreignkey",
        )

        batch_op.create_foreign_key(
            "follow_requests_requester_id_fkey",
            "users",
            ["requester_id"],
            ["id"],
        )

        batch_op.create_foreign_key(
            "follow_requests_target_id_fkey",
            "users",
            ["target_id"],
            ["id"],
        )

        batch_op.drop_constraint(
            "unique_follow_request",
            type_="unique",
        )

        batch_op.drop_index(
            "idx_follow_request_target",
        )

        batch_op.drop_index(
            "idx_follow_request_requester",
        )