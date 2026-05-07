# app/inbox/services/conversation_service.py

from sqlalchemy import func

from app.extensions import db
from app.inbox.models.conversation import Conversation
from app.inbox.models.conversation_participant import ConversationParticipant


class ConversationService:

    @staticmethod
    def get_or_create(sender_id, receiver_id):

        # -------------------------
        # NORMALIZE USER ORDER
        # -------------------------
        u1, u2 = sorted([sender_id, receiver_id])

        # -------------------------
        # FIND EXISTING CONVERSATION
        # (STRICT MATCH: exactly 2 participants)
        # -------------------------
        convo = (
            db.session.query(Conversation)
            .join(ConversationParticipant)
            .filter(ConversationParticipant.user_id.in_([u1, u2]))
            .group_by(Conversation.id)
            .having(func.count(ConversationParticipant.id) == 2)
            .first()
        )

        if convo:
            return convo

        # -------------------------
        # CREATE NEW CONVERSATION
        # -------------------------
        convo = Conversation()
        db.session.add(convo)
        db.session.flush()  # get convo.id

        # -------------------------
        # DOUBLE SAFETY CHECK (IMPORTANT)
        # prevents duplicate inserts
        # -------------------------
        existing = ConversationParticipant.query.filter_by(
            conversation_id=convo.id
        ).all()

        existing_user_ids = {p.user_id for p in existing}

        participants = []

        for uid in (u1, u2):
            if uid not in existing_user_ids:
                participants.append(
                    ConversationParticipant(
                        conversation_id=convo.id,
                        user_id=uid
                    )
                )

        db.session.add_all(participants)

        db.session.commit()
        return convo