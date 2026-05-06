# app/inbox/queries/inbox_query.py
from app.inbox.models.conversation import ConversationParticipant
from app.inbox.models.message import Message


class InboxQuery:

    @staticmethod
    def user_conversations(user_id):

        return ConversationParticipant.query.filter_by(
            user_id=user_id
        ).all()

    @staticmethod
    def conversation_messages(conversation_id):

        return Message.query.filter_by(
            conversation_id=conversation_id
        ).order_by(Message.created_at.asc()).all()