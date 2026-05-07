# app/inbox/models/conversation_hide.py

from datetime import datetime
from app.extensions import db


class ConversationHide(db.Model):
    __tablename__ = "conversation_hides"

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

    hidden_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )