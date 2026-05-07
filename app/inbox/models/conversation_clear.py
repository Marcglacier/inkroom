# app/inbox/models/conversation_clear.py

from datetime import datetime
from app.extensions import db


class ConversationClear(db.Model):
    __tablename__ = "conversation_clears"

    id = db.Column(db.Integer, primary_key=True)

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversations.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    cleared_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )