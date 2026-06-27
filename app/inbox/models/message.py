# app/inbox/models/message.py
from datetime import datetime
from sqlalchemy.dialects.postgresql import TSVECTOR
from app.extensions import db


class Message(db.Model):
    __tablename__ = "messages"

    # ================= CORE =================
    id = db.Column(db.Integer, primary_key=True)

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=True  # allow DM without conversation OR keep if required
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )

    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ================= MEDIA =================
    media_url = db.Column(db.String(500))
    media_type = db.Column(db.String(50))

    # ================= SEARCH =================
    search_vector = db.Column(TSVECTOR)

    # ================= THREADING =================
    reply_to_message_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id", ondelete="SET NULL")
    )

    reply_to = db.relationship(
        "Message",
        remote_side="Message.id",
        foreign_keys=[reply_to_message_id],
        backref="replies"
    )

    forwarded_from_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id", ondelete="SET NULL")
    )

    is_forwarded = db.Column(db.Boolean, default=False)

    # ================= STATUS =================
    edited = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default="sent")

    delivered_at = db.Column(db.DateTime)
    read_at = db.Column(db.DateTime)

    # ================= SOFT DELETE =================
    deleted_for_everyone = db.Column(db.Boolean, default=False)
    deleted_for_users = db.Column(db.JSON, default=list)
    delete_requested_at = db.Column(db.DateTime)

    backup_content = db.Column(db.Text)

    # ================= RELATIONSHIPS =================
    sender = db.relationship(
        "User",
        foreign_keys=[sender_id],
        passive_deletes=True
    )

    pins = db.relationship(
        "PinnedMessage",
        backref="message",
        lazy="select",
        cascade="all, delete-orphan"
    )


    # ================= SERIALIZER =================
    def to_dict(self):
        return {
          "id": self.id,
          "conversation_id": self.conversation_id,
          "sender_id": self.sender_id,
          "receiver_id": self.receiver_id,
          "sender_username": self.sender.username if self.sender else None,

          "content": self.content,
          "media_url": self.media_url,
          "media_type": self.media_type,
          "reply_to": self.reply_to_message_id,

          "created_at": (
              self.created_at.isoformat() + "Z"
              if self.created_at else None
            ),

          "edited": self.edited,
          "status": self.status,

          "delivered_at": (
              self.delivered_at.isoformat() + "Z"
              if self.delivered_at else None
            ),

          "read_at": (
             self.read_at.isoformat() + "Z"
             if self.read_at else None
            ),

          "is_forwarded": self.is_forwarded,
        }
    def __repr__(self):
        return f"<Message {self.id} from={self.sender_id} to={self.receiver_id}>"