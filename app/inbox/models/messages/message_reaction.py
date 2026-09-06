# app/inbox/models/message_reaction.py
from datetime import datetime
from app.extensions import db


class MessageReaction(db.Model):
    __tablename__ = "message_reactions"

    id = db.Column(db.Integer, primary_key=True)

    message_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id", ondelete="CASCADE"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    reaction = db.Column(
        db.String(10),
        nullable=False
    )  # ❤️ 👍 😂 😮 😢 🔥

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # prevent duplicate reactions
    __table_args__ = (
        db.UniqueConstraint("message_id", "user_id"),
    )

    message = db.relationship("Message", backref="reactions")