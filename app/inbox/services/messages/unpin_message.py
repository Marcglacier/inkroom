# app/inbox/services/messages/unpin_message.py

from app.extensions import db, socketio
from app.inbox.models.messages.message import Message
from app.inbox.models.conversations.conversation_participant import ConversationParticipant
from app.inbox.models.messages.pinned_message import PinnedMessage
from app.inbox.services.settings.blocks.block_policy import BlockPolicy
from app.inbox.services.messages.create_system_message import (
    create_system_message,
)
from app.inbox.serializers.message_serializer import MessageSerializer


def unpin_message(user_id, message_id):
    pin = PinnedMessage.query.filter_by(
        message_id=message_id
    ).first()

    if not pin:
        return {"error": "not pinned"}, 404

    participants = ConversationParticipant.query.filter_by(
        conversation_id=pin.conversation_id
    ).all()

    if not any(p.user_id == user_id for p in participants):
        return {"error": "Conversation not found"}, 404

    message = db.session.get(Message, message_id)
    if not message:
        return {"error": "Message not found"}, 404

    other_ids = {
        p.user_id for p in participants
        if p.user_id is not None and p.user_id != user_id
    }

    if any(
        BlockPolicy.blocks_either_user(user_id, other_id)
        for other_id in other_ids
    ):
        return {"error": "Unpinning is unavailable"}, 403

    payload = {
        "message_id": pin.message_id,
        "conversation_id": pin.conversation_id,
        "is_pinned": False,
    }

    system = create_system_message(
        conversation_id=pin.conversation_id,
        sender_id=user_id,
        event="message_unpinned",
        target_message_id=pin.message_id,
    )

    db.session.delete(pin)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    socketio.emit(
        "message:unpinned",
        payload,
        room=f"conversation_{pin.conversation_id}",
    )
    socketio.emit(
        "message:new",
        MessageSerializer(system).to_dict(),
        room=f"conversation_{pin.conversation_id}",
    )

    return {
        "message": "unpinned",
        **payload,
    }
