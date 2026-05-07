# app/inbox/services/conversation_service.py

from app.extensions import db
from app.inbox.models.conversation import Conversation
from app.inbox.models.conversation_participant import ConversationParticipant


class ConversationService:

    @staticmethod
    def get_or_create(sender_id, receiver_id):

        # -------------------------
        # NORMALIZE USERS (NO HELPER)
        # -------------------------
        u1, u2 = sorted([sender_id, receiver_id])

        # -------------------------
        # FIND EXISTING CONVERSATION
        # -------------------------
        convo = (
            db.session.query(Conversation)
            .join(ConversationParticipant)
            .filter(
                ConversationParticipant.user_id.in_([u1, u2])
            )
            .group_by(Conversation.id)
            .having(db.func.count(Conversation.id) == 2)
            .first()
        )

        if convo:
            return convo

        # -------------------------
        # CREATE NEW CONVERSATION
        # -------------------------
        convo = Conversation()
        db.session.add(convo)
        db.session.flush()

        db.session.add_all([
            ConversationParticipant(
                conversation_id=convo.id,
                user_id=u1
            ),
            ConversationParticipant(
                conversation_id=convo.id,
                user_id=u2
            ),
        ])

        db.session.commit()
        return convo