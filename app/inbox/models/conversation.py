# app/inbox/models/conversation.py

from datetime import datetime
from app.extensions import db


class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # metadata
    status = db.Column(db.String(20), default="active")
    type = db.Column(db.String(20), default="dm")
    deleted_at = db.Column(db.DateTime, nullable=True)

    # =========================
    # RELATIONSHIPS
    # =========================

    participants = db.relationship(
        "ConversationParticipant",
        backref="conversation",
        lazy="joined",
        cascade="all, delete-orphan",
    )

    # =========================
    # CORE LOGIC
    # =========================

    @staticmethod
    def get_or_create(user_a_id, user_b_id):
        """
        Find an existing DM conversation between two users
        or create a new one.
        """

        from sqlalchemy import func
        from app.inbox.models.conversation_participant import ConversationParticipant

        # find DM conversation containing BOTH users
        conversation = (
            db.session.query(Conversation)
            .join(ConversationParticipant)
            .filter(Conversation.type == "dm")
            .filter(ConversationParticipant.user_id.in_([user_a_id, user_b_id]))
            .group_by(Conversation.id)
            .having(func.count(ConversationParticipant.id) == 2)
            .first()
        )

        if conversation:
            return conversation

        # create new conversation
        conversation = Conversation(type="dm")
        db.session.add(conversation)
        db.session.flush()  # get conversation.id

        db.session.add_all(
            [
                ConversationParticipant(
                    conversation_id=conversation.id,
                    user_id=user_a_id,
                ),
                ConversationParticipant(
                    conversation_id=conversation.id,
                    user_id=user_b_id,
                ),
            ]
        )

        db.session.commit()

        return conversation