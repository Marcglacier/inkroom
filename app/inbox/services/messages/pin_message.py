# app/inbox/services/messages/pin_message.py
from datetime import datetime
from app.extensions import db
from app.inbox.models.pinned_message import PinnedMessage
from app.inbox.models.message import Message


def pin_message(user_id, message_id):

    msg = Message.query.get(message_id)

    if not msg:
        return {"error": "message not found"}, 404

    already = PinnedMessage.query.filter_by(
        message_id=message_id
    ).first()

    if already:
        return {"error": "already pinned"}, 400

    pin = PinnedMessage(
        conversation_id=msg.conversation_id,
        message_id=message_id,
        pinned_by=user_id,
        pinned_at=datetime.utcnow()
    )

    db.session.add(pin)
    db.session.commit()

    return {"message": "pinned"}