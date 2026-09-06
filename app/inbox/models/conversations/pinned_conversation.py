# app/inbox/models/pinned_conversation.py

from app import db
from datetime import datetime


class PinnedConversation(db.Model):
    __tablename__ = "pinned_conversations"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversations.id", ondelete="CASCADE"),
        primary_key=True,
    )

    pinned_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )