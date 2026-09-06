# app/inbox/services/messages/fetch_messages.py

import time

from app.inbox.models.messages.message import Message
from app.models.user import User
from app.inbox.services.messages.message_reaction_aggregator import build_reactions
from app.inbox.serializers.message_media_serializer import MessageMediaSerializer
from app.inbox.models.conversations.conversation_clear import ConversationClear

def fetch_messages(
    conversation_id,
    current_user_id,
    limit=15,
    offset=0,
):
    overall = time.perf_counter()

    # ---------------------------------------------------------
    # Conversation clear
    # ---------------------------------------------------------
    clear = ConversationClear.query.filter_by(
        conversation_id=conversation_id,
        user_id=current_user_id,
    ).first()

    # ---------------------------------------------------------
    # IMPORTANT:
    # Fetch newest messages FIRST.
    #
    # We fetch one extra message so the caller knows whether
    # another page exists.
    # ---------------------------------------------------------
    query = Message.query.filter(
        Message.conversation_id == conversation_id,
        Message.deleted_for_everyone.is_(False),
    )

    if clear:
        query = query.filter(
            Message.created_at > clear.cleared_at
        )

    query = (
        query
        .order_by(Message.created_at.desc())
        .offset(offset)
        .limit(limit + 1)
    )

    # THIS IS NOW ONLY limit + 1 messages.
    db_messages = query.all()

    print(
        "FETCH SQL:",
        f"limit={limit}",
        f"offset={offset}",
        f"rows={len(db_messages)}",
    )

    # ---------------------------------------------------------
    # Determine whether another page exists
    # ---------------------------------------------------------
    has_more = len(db_messages) > limit

    # Remove the extra message
    db_messages = db_messages[:limit]

    # We fetched newest -> oldest.
    # The UI wants oldest -> newest.
    db_messages.reverse()

    messages = []

    message_cache = {}
    user_cache = {}

    def get_user(user_id):
        if user_id not in user_cache:
            user_cache[user_id] = User.query.get(user_id)

        return user_cache[user_id]

    def get_message(msg_id):
        if msg_id not in message_cache:
            message_cache[msg_id] = Message.query.get(msg_id)

        return message_cache[msg_id]

    # ---------------------------------------------------------
    # Build response
    # ---------------------------------------------------------
    for message in db_messages:

        # Skip messages deleted only for this user
        if current_user_id in (message.deleted_for_users or []):
            continue

        sender = get_user(message.sender_id)

        sender_username = ( sender.username if sender else "deleted_user" )

        sender_name = (
            sender.name
            if sender else "Deleted User"
        )

        # -----------------------------------------------------
        # Reply
        # -----------------------------------------------------
        reply_data = None

        if message.reply_to_message_id:

            replied_msg = get_message(
                message.reply_to_message_id
            )

            if (
                replied_msg
                and not replied_msg.deleted_for_everyone
            ):
                reply_sender = get_user(
                    replied_msg.sender_id
                )

                reply_data = {
                    "id": replied_msg.id,
                    "content": replied_msg.content,
                    "sender_id": replied_msg.sender_id,
                    "sender_name": (
                        reply_sender.name
                        if reply_sender
                        else "Deleted User"
                    ),
                    "sender_username": (
                        reply_sender.username
                        if reply_sender
                        else "deleted_user"
                    ),
                }

        # -----------------------------------------------------
        # Reactions
        # -----------------------------------------------------
        reactions = build_reactions(message.id)

        # -----------------------------------------------------
        # Media
        # -----------------------------------------------------
        media = [
            MessageMediaSerializer(media).to_dict()
            for media in message.media
        ]

        messages.append({
            "id": message.id,
            "content": message.content,

            "message_type": message.message_type,
            "system_event": message.system_event,
            "target_message_id": message.target_message_id,

            "media": media,
            "links": [ link.to_dict() for link in message.links ],
            "sender_id": message.sender_id,
            "sender_username": sender_username,
            "sender_name": sender_name,

            "created_at": message.created_at,

            "edited": message.edited,

            "status": message.status,
            "delivered_at": message.delivered_at,
            "read_at": message.read_at,

            "is_sender": (
                message.sender_id == current_user_id
            ),

            "is_forwarded": message.is_forwarded,
            "forwarded_from_id": message.forwarded_from_id,

            "deleted_for_everyone": (
                message.deleted_for_everyone
            ),

            "reply_to": reply_data,
            "reactions": reactions,
        })

    print(
        f"FETCH TOTAL: "
        f"{time.perf_counter() - overall:.6f}s"
    )

    return messages, has_more