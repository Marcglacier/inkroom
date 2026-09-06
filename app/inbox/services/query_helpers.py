# app/inbox/services/query_helpers.py
from app.inbox.models.messages.message import Message


def unread_messages(user_id, conversation_id):

    return Message.query.filter(
        Message.conversation_id == conversation_id,
        Message.sender_id != user_id,
        Message.read_at.is_(None),
        Message.deleted_for_everyone.is_(False)
    )