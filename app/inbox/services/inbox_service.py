# app/inbox/services/inbox_service.py
from app.inbox.models.conversation import Conversation
from app.inbox.models.conversation_participant import ConversationParticipant
from app.inbox.models.message import Message
from app.models.user import User
from app.inbox.services.query_helpers import unread_messages


class InboxService:

    @staticmethod
    def get_inbox(user_id):

        convos = ConversationParticipant.query.filter_by(
            user_id=user_id
        ).all()

        results = []

        for p in convos:

            convo = Conversation.query.get(p.conversation_id)

            other = ConversationParticipant.query.filter(
                ConversationParticipant.conversation_id == convo.id,
                ConversationParticipant.user_id != user_id
            ).first()

            other_user = User.query.get(other.user_id)

            last_msg = Message.query.filter_by(
                conversation_id=convo.id
            ).order_by(Message.created_at.desc()).first()

            unread_count = unread_messages(user_id, convo.id).count()

            results.append({
                "conversation_id": convo.id,
                "user_id": other_user.id,
                "username": other_user.username,
                "last_message": last_msg.content if last_msg else None,
                "unread": unread_count
            })

        return results