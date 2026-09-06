# app/inbox/services/messages/create_system_message.py
from app.extensions import db
from app.inbox.models.messages.message import Message


def create_system_message(
    conversation_id,
    sender_id,
    event,
    target_message_id=None,
):
    msg = Message(
        conversation_id=conversation_id,
        sender_id=sender_id,
        receiver_id=None,
        message_type="system",
        system_event=event,
        target_message_id=target_message_id,
        content=None,
        status="sent",
    )

    db.session.add(msg)
    db.session.commit()

    return msg