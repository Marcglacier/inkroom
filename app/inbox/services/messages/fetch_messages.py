# app/inbox/services/messages/fetch_messages.py
from app.inbox.models.message import Message


def fetch_messages(conversation_id, current_user_id=None):

    msgs = (
        Message.query
        .filter_by(conversation_id=conversation_id)
        .order_by(Message.created_at.asc())
        .all()
    )

    results = []

    for m in msgs:

        is_sender = (m.sender_id == current_user_id)

        base = {
            "id": m.id,
            "sender_id": m.sender_id,
            "content": m.content,
            "created_at": m.created_at,
            "edited": m.edited,
            "is_sender": is_sender
        }

        if is_sender:
            base.update({
                "status": m.status,
                "delivered_at": m.delivered_at,
                "read_at": m.read_at
            })

        results.append(base)

    return results