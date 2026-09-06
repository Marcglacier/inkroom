# app/inbox/services/inbox/get_last_message.py

from app.inbox.models.messages.message import Message


def get_last_message(conversation_id):

    msg = (
        Message.query
        .filter(
            Message.conversation_id == conversation_id,
            Message.deleted_for_everyone.is_(False)
        )
        .order_by(Message.created_at.desc())
        .first()
    )

    return msg.content if msg else None