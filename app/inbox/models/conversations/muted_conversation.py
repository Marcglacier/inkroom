# app/inbox/models/conversations/muted_conversation.py
from datetime import datetime
from app.extensions import db


class MutedConversation(db.Model):
    __tablename__ = "muted_conversation"

    __table_args__ = (
        db.UniqueConstraint(
            "conversation_id",
            "user_id",
            name="uq_muted_conversation",
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    is_always = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )

    muted_until = db.Column(
        db.DateTime,
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )