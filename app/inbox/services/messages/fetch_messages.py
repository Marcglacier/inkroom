# app/inbox/services/messages/fetch_messages.py

from app.inbox.models.message import Message
from app.models.user import User
from app.inbox.services.messages.message_reaction_aggregator import build_reactions


def fetch_messages(conversation_id, current_user_id):

    query = Message.query.filter_by(
        conversation_id=conversation_id
    ).order_by(Message.created_at.asc())

    messages = []

    # =============================
    # CACHE (avoid repeated DB hits)
    # =============================
    message_cache = {}
    user_cache = {}

    for message in query:

        # -----------------------------
        # DELETE FOR EVERYONE
        # -----------------------------
        if message.deleted_for_everyone:
            continue

        # -----------------------------
        # DELETE FOR ME
        # -----------------------------
        if current_user_id in (message.deleted_for_users or []):
            continue

        # =============================
        # SENDER USERNAME (CACHE)
        # =============================
        sender_id = message.sender_id

        if sender_id in user_cache:
            sender = user_cache[sender_id]
        else:
            sender = User.query.get(sender_id)
            user_cache[sender_id] = sender

        sender_username = sender.username if sender else None

        # =============================
        # REPLY OBJECT
        # =============================
        reply_data = None

        if message.reply_to_message_id:

            if message.reply_to_message_id in message_cache:
                replied_msg = message_cache[message.reply_to_message_id]
            else:
                replied_msg = Message.query.get(message.reply_to_message_id)
                message_cache[message.reply_to_message_id] = replied_msg

            if replied_msg and not replied_msg.deleted_for_everyone:

                reply_sender_id = replied_msg.sender_id

                if reply_sender_id in user_cache:
                    reply_sender = user_cache[reply_sender_id]
                else:
                    reply_sender = User.query.get(reply_sender_id)
                    user_cache[reply_sender_id] = reply_sender

                reply_data = {
                    "id": replied_msg.id,
                    "content": replied_msg.content,
                    "sender_username": reply_sender.username if reply_sender else "unknown"
                }

        # =============================
        # MESSAGE RESPONSE
        # =============================
        messages.append({
            "id": message.id,
            "content": message.content,

            "media_url": message.media_url,
            "media_type": message.media_type,

            "sender_id": message.sender_id,
            "sender_username": sender_username,

            "created_at": message.created_at,
            "edited": message.edited,

            "status": message.status,
            "delivered_at": message.delivered_at,
            "read_at": message.read_at,

            "is_sender": message.sender_id == current_user_id,

            "is_forwarded": message.is_forwarded,
            "forwarded_from_id": message.forwarded_from_id,

            "reply_to": reply_data,

            "reactions": build_reactions(message.id)
        })

    return messages