from datetime import datetime

from app.extensions import db


class ConversationRequest(db.Model):

    __tablename__ = "conversation_requests"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversations.id"),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="pending",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    sender = db.relationship(
        "User",
        foreign_keys=[sender_id]
    )

    receiver = db.relationship(
        "User",
        foreign_keys=[receiver_id]
    )

    conversation = db.relationship(
        "Conversation",
        foreign_keys=[conversation_id]
    )

    __table_args__ = (
        db.UniqueConstraint(
            "sender_id",
            "receiver_id",
            name="unique_conversation_request"
        ),
    )