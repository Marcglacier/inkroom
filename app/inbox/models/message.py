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

    content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # =========================
    # FULL TEXT SEARCH
    # =========================
    search_vector = db.Column(TSVECTOR)

    # =========================
    # REPLY SYSTEM
    # =========================
    reply_to_message_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id", ondelete="SET NULL"),
        nullable=True
    )

    reply_to = db.relationship(
        "Message",
        remote_side="Message.id",
        foreign_keys=[reply_to_message_id],
        backref="replies",
        lazy=True
    )

    # =========================
    # EDITING
    # =========================
    edited = db.Column(db.Boolean, default=False)

    # =========================
    # DELIVERY SYSTEM
    # =========================
    status = db.Column(db.String(20), default="sent")
    delivered_at = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)

    # =========================
    # DELETE SYSTEM
    # =========================
    deleted_for_everyone = db.Column(db.Boolean, default=False)

    deleted_for_users = db.Column(
        db.JSON,
        default=lambda: []
    )

    delete_requested_at = db.Column(db.DateTime)

    # =========================
    # BACKUP CONTENT
    # =========================
    backup_content = db.Column(db.Text)

    # =========================
    # FORWARDING SYSTEM
    # =========================
    forwarded_from_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id"),
        nullable=True
    )

    is_forwarded = db.Column(db.Boolean, default=False)

    # =========================
    # RELATIONSHIPS
    # =========================
    sender = db.relationship("User", lazy=True)

    def __repr__(self):
        return f"<Message {self.id} sender={self.sender_id}>"