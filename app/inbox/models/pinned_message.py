# app/inbox/models/pinned_message.py

from datetime import datetime
from app.extensions import db


class PinnedMessage(db.Model):
    __tablename__ = "pinned_messages"

    __table_args__ = (
      db.UniqueConstraint(
          "message_id",
          name="uq_pinned_message",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversations.id"),
        nullable=False
    )

    message_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id", ondelete="CASCADE"),
        nullable=False
    )

    pinned_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    pinned_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )