# app/inbox/models/message.py

from datetime import datetime
from sqlalchemy.dialects.postgresql import TSVECTOR
from app.extensions import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)

    conversation_id = db.Column(
        db.Integer, db.ForeignKey("conversations.id"), nullable=False
    )

    sender_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )

    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # media
    media_url = db.Column(db.String(500))
    media_type = db.Column(db.String(50))

    # search
    search_vector = db.Column(TSVECTOR)

    # reply
    reply_to_message_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id", ondelete="SET NULL"),
    )

    reply_to = db.relationship(
        "Message",
        remote_side="Message.id",
        foreign_keys=[reply_to_message_id],
        backref="replies",
    )

    # editing
    edited = db.Column(db.Boolean, default=False)

    # delivery
    status = db.Column(db.String(20), default="sent")
    delivered_at = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)

    # delete
    deleted_for_everyone = db.Column(db.Boolean, default=False)

    deleted_for_users = db.Column(
        db.JSON,
        default=lambda: []
    )

    delete_requested_at = db.Column(db.DateTime)

    # backup
    backup_content = db.Column(db.Text)

    # forwarding
    forwarded_from_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id"),
    )

    is_forwarded = db.Column(db.Boolean, default=False)

    # relationships
    sender = db.relationship("User", lazy=True)

    # serializer
    def to_dict(self):
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "sender_id": self.sender_id,
            "sender_username": self.sender.username if self.sender else None,
            "content": self.content,
            "media_url": self.media_url,
            "media_type": self.media_type,
            "reply_to": self.reply_to_message_id,
            "created_at": self.created_at,
            "edited": self.edited,
            "status": self.status,
            "delivered_at": self.delivered_at,
            "read_at": self.read_at,
            "is_forwarded": self.is_forwarded,
        }

    def __repr__(self):
        return f"<Message {self.id} sender={self.sender_id}>"