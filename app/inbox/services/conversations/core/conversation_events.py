
# app/inbox/services/conversations/core/conversation_events.py

from app.extensions import socketio
from app.models.settings.user_restriction import UserRestriction

from app.inbox.models.conversations.conversation import Conversation
from app.inbox.services.conversations.core.conversation_builder import (
    ConversationCardBuilder,
)


def emit_conversation_updated(conversation_id: int):
    """Sync inbox cards without exposing restricted chats in the normal inbox."""

    conversation = Conversation.query.get(conversation_id)

    if not conversation:
        return

    participants = conversation.participants

    for participant in participants:
        user_id = participant.user_id

        if user_id is None:
            continue

        # A restriction hides this active DM only from the restricter.
        if conversation.type == "dm" and conversation.status == "active":
            other_user_ids = [
                item.user_id
                for item in participants
                if item.user_id is not None
                and item.user_id != user_id
            ]

            restricted_chat = any(
                UserRestriction.query.filter_by(
                    restricter_id=user_id,
                    restricted_id=other_user_id,
                ).first()
                is not None
                for other_user_id in other_user_ids
            )

            if restricted_chat:
                continue

        card = ConversationCardBuilder(
            conversation,
            user_id,
        ).build()

        if not card:
            continue

        socketio.emit(
            "conversation:updated",
            card,
            room=f"user_{user_id}",
        )
