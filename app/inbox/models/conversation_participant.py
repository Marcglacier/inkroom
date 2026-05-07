# app/inbox/models/conversation_participant.py

from app.extensions import db


class ConversationParticipant(db.Model):
    __tablename__ = "conversation_participants"

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

    # Prevent duplicate participants in the same conversation
    __table_args__ = (
        db.UniqueConstraint(
            "conversation_id",
            "user_id",
            name="unique_conversation_participant"
        ),
    )