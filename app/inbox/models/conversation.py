# app/inbox/models/conversation.py

from datetime import datetime
from sqlalchemy import func

from app.extensions import db


class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(20),
        default="active"
    )  # active | pending | rejected

    type = db.Column(
        db.String(20),
        default="dm"
    )

    deleted_at = db.Column(
        db.DateTime,
        nullable=True
    )

    participants = db.relationship(
        "ConversationParticipant",
        backref="conversation",
        lazy="joined",
        cascade="all, delete-orphan"
    )

    @staticmethod
    def find_between_users(
        user_a_id,
        user_b_id
    ):
        from app.inbox.models.conversation_participant import (
            ConversationParticipant
        )

        return (
            db.session.query(Conversation)
            .join(ConversationParticipant)
            .filter(
                Conversation.type == "dm"
            )
            .filter(
                ConversationParticipant.user_id.in_(
                    [user_a_id, user_b_id]
                )
            )
            .group_by(
                Conversation.id
            )
            .having(
                func.count(
                    ConversationParticipant.id
                ) == 2
            )
            .first()
        )

    @staticmethod
    def get_or_create(
        user_a_id,
        user_b_id
    ):
        from app.inbox.models.conversation_participant import (
            ConversationParticipant
        )

        convo = Conversation.find_between_users(
            user_a_id,
            user_b_id
        )

        if convo:
            return convo

        convo = Conversation(
            type="dm",
            status="active"
        )

        db.session.add(convo)
        db.session.flush()

        db.session.add_all([
            ConversationParticipant(
                conversation_id=convo.id,
                user_id=user_a_id
            ),
            ConversationParticipant(
                conversation_id=convo.id,
                user_id=user_b_id
            )
        ])

        db.session.commit()

        return convo

    @staticmethod
    def create_request(
        user_a_id,
        user_b_id
    ):
        from app.inbox.models.conversation_participant import (
            ConversationParticipant
        )

        convo = Conversation.find_between_users(
            user_a_id,
            user_b_id
        )

        if convo:
            return convo

        convo = Conversation(
            type="dm",
            status="pending"
        )

        db.session.add(convo)
        db.session.flush()

        db.session.add_all([
            ConversationParticipant(
                conversation_id=convo.id,
                user_id=user_a_id
            ),
            ConversationParticipant(
                conversation_id=convo.id,
                user_id=user_b_id
            )
        ])

        db.session.commit()

        return convo