# app/inbox/services/conversations/conversation_service.py
from sqlalchemy import func

from app.extensions import db
from app.inbox.models.conversation import Conversation
from app.inbox.models.conversation_participant import ConversationParticipant


class ConversationService:

    @staticmethod
    def get_or_create(sender_id, receiver_id):

        # =========================
        # SELF CHAT (Saved Messages)
        # =========================
        if sender_id == receiver_id:

            convo = (
                db.session.query(Conversation)
                .join(ConversationParticipant)
                .filter(Conversation.type == "self")
                .filter(ConversationParticipant.user_id == sender_id)
                .group_by(Conversation.id)
                .first()
            )

            if convo:
                return convo

            convo = Conversation(type="self")
            db.session.add(convo)
            db.session.flush()

            db.session.add(
                ConversationParticipant(
                    conversation_id=convo.id,
                    user_id=sender_id
                )
            )

            db.session.commit()
            return convo

        # =========================
        # NORMAL CHAT (DM BETWEEN 2 USERS)
        # =========================
        u1, u2 = sorted([sender_id, receiver_id])

        convo = (
            db.session.query(Conversation)
            .join(ConversationParticipant)
            .filter(Conversation.type == "dm")
            .filter(ConversationParticipant.user_id.in_([u1, u2]))
            .group_by(Conversation.id)
            .having(func.count(ConversationParticipant.id) == 2)
            .first()
        )

        if convo:
            return convo

        # =========================
        # CREATE NEW DM CONVERSATION
        # =========================
        convo = Conversation(type="dm")
        db.session.add(convo)
        db.session.flush()

        db.session.add_all([
            ConversationParticipant(conversation_id=convo.id, user_id=u1),
            ConversationParticipant(conversation_id=convo.id, user_id=u2),
        ])

        db.session.commit()
        return convo