"""add message full text search

Revision ID: 36d90c3001d1
Revises: dc5422992c92
Create Date: 2026-05-11 18:10:11.240436
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers
revision = '36d90c3001d1'
down_revision = 'dc5422992c92'
branch_labels = None
depends_on = None


def upgrade():

    # Add search vector column
    with op.batch_alter_table('messages') as batch_op:
        batch_op.add_column(
            sa.Column('search_vector', postgresql.TSVECTOR(), nullable=True)
        )

    # Populate search vector with message content + sender username
    op.execute("""
        UPDATE messages
        SET search_vector =
            to_tsvector('english', coalesce(content,'')) ||
            to_tsvector(
                'english',
                (SELECT username FROM users WHERE users.id = messages.sender_id)
            );
    """)

    # Create GIN index for fast search
    op.execute("""
        CREATE INDEX idx_messages_search
        ON messages
        USING GIN(search_vector);
    """)

    # Create trigger function
    op.execute("""
        CREATE FUNCTION message_search_trigger()
        RETURNS trigger AS $$
        BEGIN
            NEW.search_vector :=
                to_tsvector('english', coalesce(NEW.content,'')) ||
                to_tsvector(
                    'english',
                    (SELECT username FROM users WHERE users.id = NEW.sender_id)
                );
            RETURN NEW;
        END
        $$ LANGUAGE plpgsql;
    """)

    # Attach trigger
    op.execute("""
        CREATE TRIGGER message_search_update
        BEFORE INSERT OR UPDATE
        ON messages
        FOR EACH ROW
        EXECUTE FUNCTION message_search_trigger();
    """)


def downgrade():

    # Remove trigger
    op.execute("""
        DROP TRIGGER IF EXISTS message_search_update
        ON messages;
    """)

    # Remove trigger function
    op.execute("""
        DROP FUNCTION IF EXISTS message_search_trigger;
    """)

    # Remove index
    op.execute("""
        DROP INDEX IF EXISTS idx_messages_search;
    """)

    # Drop column
    with op.batch_alter_table('messages') as batch_op:
        batch_op.drop_column('search_vector')