# app/inbox/services/conversations/conversation_service.py
from sqlalchemy import func
from app.extensions import db
from app.inbox.models.conversations.conversation import Conversation
from app.inbox.models.conversations.conversation_participant import ConversationParticipant


class ConversationService:

    @staticmethod
    def get_or_create(user_a, user_b):

        # find existing conversation with EXACTLY these 2 users
        convo = (
            db.session.query(Conversation)
            .join(ConversationParticipant)
            .filter(Conversation.type == "dm")
            .group_by(Conversation.id)
            .having(
                func.count(ConversationParticipant.id) == 2
            )
            .filter(
                ConversationParticipant.user_id.in_([user_a, user_b])
            )
            .first()
        )

        if convo:
            return convo

        # create conversation
        convo = Conversation(type="dm")
        db.session.add(convo)
        db.session.flush()

        db.session.add_all([
            ConversationParticipant(conversation_id=convo.id, user_id=user_a),
            ConversationParticipant(conversation_id=convo.id, user_id=user_b),
        ])

        db.session.commit()
        return convo