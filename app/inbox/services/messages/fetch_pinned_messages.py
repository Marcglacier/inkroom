# app/inbox/services/messages/fetch_pinned_messages.py
from app.inbox.models.pinned_message import PinnedMessage
from app.inbox.models.message import Message
from app.models.user import User


def fetch_pinned(conversation_id):

    pins = PinnedMessage.query.filter_by(
        conversation_id=conversation_id
    ).all()

    results = []

    for p in pins:

        msg = Message.query.get(p.message_id)

        if not msg:
            continue

        sender = User.query.get(msg.sender_id)
        pinner = User.query.get(p.pinned_by)

        results.append({
            "message_id": msg.id,
            "content": msg.content,
            "sender": {
                "id": sender.id,
                "username": sender.username
            } if sender else None,
            "pinned_by": {
                "id": pinner.id,
                "username": pinner.username
            } if pinner else None,
            "pinned_at": p.pinned_at
        })

    return results