# app/inbox/services/conversations/conversation_events.py

from app.extensions import socketio

from app.inbox.models.conversations.conversation import Conversation
from app.inbox.services.conversations.core.conversation_builder import (
    ConversationCardBuilder
)


def emit_conversation_updated(conversation_id: int):
    """
    Sync inbox cards after conversation state changes.

    Triggered by:
    - new messages
    - message edits
    - message deletes
    - reactions
    - pins/unpins
    - read state changes
    """

    conversation = Conversation.query.get(conversation_id)

    if not conversation:
        return

    for participant in conversation.participants:

        card = ConversationCardBuilder(
            conversation,
            participant.user_id,
        ).build()

        if not card:
            continue

        socketio.emit(
            "conversation:updated",
            card,
            room=f"user_{participant.user_id}",
        )