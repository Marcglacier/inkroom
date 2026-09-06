# app/inbox/services/messages/pin_message.py
from datetime import datetime
from app.extensions import db, socketio
from app.inbox.models.messages.pinned_message import PinnedMessage
from app.inbox.models.messages.message import Message
from app.inbox.models.conversations.conversation import Conversation
from app.inbox.services.messages.create_system_message import create_system_message
from app.inbox.serializers.message_serializer import MessageSerializer

def pin_message(user_id, message_id):

    msg = Message.query.get(message_id)

    if not msg:
        return {"error": "message not found"}, 404

    already = PinnedMessage.query.filter_by(
        message_id=message_id
    ).first()

    if already:
        return {"error": "already pinned"}, 400
    
    convo = Conversation.query.get(msg.conversation_id)
    if not convo:
        return {"error": "Conversation not found"}, 404

    if user_id not in [p.user_id for p in convo.participants]:
        return {"error": "Forbidden"}, 403
    
    pin_count = PinnedMessage.query.filter_by(
        conversation_id=msg.conversation_id
    ).count()

    if pin_count >= 5:
       return {
          "error": "Maximum of 5 pinned messages allowed."
        }, 400

    pin = PinnedMessage(
        conversation_id=msg.conversation_id,
        message_id=message_id,
        pinned_by=user_id,
        pinned_at=datetime.utcnow()
    )

    db.session.add(pin)
    db.session.commit()
    system = create_system_message(
        conversation_id=msg.conversation_id,
        sender_id=user_id,
        event="message_pinned",
        target_message_id=msg.id,
    )

    payload = {
        "message_id": msg.id,
        "conversation_id": msg.conversation_id,
        "is_pinned": True,
    }

    socketio.emit(
       "message:pinned",
       payload,
       room=f"conversation_{msg.conversation_id}",
    )
    socketio.emit(
        "message:new",
        MessageSerializer(system).to_dict(),
        room=f"conversation_{msg.conversation_id}",
    )

    payload["message"] = "pinned"
    return payload