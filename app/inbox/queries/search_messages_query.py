# app/inbox/queries/search_messages_query.py
from app.inbox.models.messages.message import Message
from app.inbox.models.conversations.conversation_participant import ConversationParticipant
from app.inbox.models.conversations.conversation_clear import ConversationClear


def search_conversation(user_id, conversation_id, text):

    last_clear = (
        ConversationClear.query
        .filter_by(
            user_id=user_id,
            conversation_id=conversation_id
        )
        .order_by(ConversationClear.cleared_at.desc())
        .first()
    )

    query = Message.query.filter(
        Message.conversation_id == conversation_id,
        Message.content.ilike(f"%{text}%")
    )

    # IMPORTANT FIX: apply visibility rule AFTER search
    if last_clear:
        query = query.filter(
            Message.created_at > last_clear.cleared_at
        )

    return query.order_by(Message.created_at.desc()).all()