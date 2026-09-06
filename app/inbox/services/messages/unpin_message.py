# app/inbox/services/messages/unpin_message.py
from app.extensions import db, socketio
from app.inbox.models.messages.pinned_message import PinnedMessage
from app.inbox.services.messages.create_system_message import create_system_message
from app.inbox.serializers.message_serializer import MessageSerializer


def unpin_message(user_id, message_id):

    pin = PinnedMessage.query.filter_by(
        message_id=message_id
    ).first()

    if not pin:
        return {"error": "not pinned"}, 404

    db.session.delete(pin)
    db.session.commit()

    system = create_system_message(
        conversation_id=pin.conversation_id,
        sender_id=user_id,
        event="message_unpinned",
        target_message_id=pin.message_id,
    )

    payload = {
       "message_id": pin.message_id,
       "conversation_id": pin.conversation_id,
       "is_pinned": False,
    }

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
        "message_id": pin.message_id,
        "conversation_id": pin.conversation_id,
        "is_pinned": False,
        
    }
