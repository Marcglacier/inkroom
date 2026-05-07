# app/inbox/services/messages/fetch_messages.py
from app.inbox.models.message import Message
from app.inbox.models.conversation_clear import ConversationClear


def fetch_messages(conversation_id, current_user_id):

    query = Message.query.filter_by(
        conversation_id=conversation_id
    ).order_by(Message.created_at.asc())

    messages = []

    for message in query:

        # -----------------------------
        # DELETE FOR EVERYONE
        # -----------------------------
        if message.deleted_for_everyone:
            continue

        # -----------------------------
        # DELETE FOR ME
        # -----------------------------
        deleted_users = message.deleted_for_users or []

        if current_user_id in deleted_users:
            continue

        messages.append({
            "id": message.id,
            "content": message.content,
            "sender_id": message.sender_id,
            "created_at": message.created_at,
            "edited": message.edited,
            "status": message.status,
            "delivered_at": message.delivered_at,
            "read_at": message.read_at,
            "is_sender": message.sender_id == current_user_id
        })

    return messages