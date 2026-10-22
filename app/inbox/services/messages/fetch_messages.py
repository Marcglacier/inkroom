# app/inbox/services/messages/fetch_messages.py

import time
from app.inbox.models.messages.message import Message
from app.models.user import User
from app.models.settings.user_block import UserBlock
from app.inbox.services.messages.message_reaction_aggregator import build_reactions
from app.inbox.serializers.message_media_serializer import MessageMediaSerializer
from app.inbox.models.conversations.conversation_clear import ConversationClear
from app.inbox.services.messages.read_receipt_policy import (
    ReadReceiptPolicy,
)

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

    receipt_policy = ReadReceiptPolicy(conversation_id)

    messages = []


    message_cache = {}
    user_cache = {}
    identity_cache = {}

    def get_user(user_id):
        if user_id not in user_cache:
            user_cache[user_id] = (
                User.query.get(user_id)
                if user_id is not None
                else None
            )

        return user_cache[user_id]

    def get_display_identity(user_id):
        if user_id not in identity_cache:
            user = get_user(user_id)

            hidden = (
                user_id is not None
                and UserBlock.query.filter_by(
                    blocker_id=user_id,
                    blocked_id=current_user_id,
                ).first() is not None
            )

            if hidden:
                identity_cache[user_id] = (
                    "Deleted Account",
                    "deleted_account",
                )
            elif user:
                identity_cache[user_id] = (
                    user.name or "Deleted User",
                    user.username or "deleted_user",
                )
            else:
                identity_cache[user_id] = (
                    "Deleted User",
                    "deleted_user",
                )

        return identity_cache[user_id]
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

        sender_name, sender_username = get_display_identity(
            message.sender_id
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
                reply_name, reply_username = get_display_identity(
                    replied_msg.sender_id
                )

                reply_data = {
                    "id": replied_msg.id,
                    "content": replied_msg.content,
                    "sender_id": replied_msg.sender_id,
                    "sender_name": reply_name,
                    "sender_username": reply_username,
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
            "call_id": message.call_id,
            "call_type": message.call_type,
            "media": media,
            "links": [ link.to_dict() for link in message.links ],
            "sender_id": message.sender_id,
            "sender_username": sender_username,
            "sender_name": sender_name,

            "created_at": message.created_at,

            "edited": message.edited,

            "status": receipt_policy.message_status(message),
            "delivered_at": message.delivered_at,
            "read_at": receipt_policy.read_at(message),

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