# app/inbox/services/conversations/conversation_events.py

from app.extensions import socketio

from app.inbox.models.conversation import Conversation
from app.inbox.services.conversations.conversation_builder import (
    build_conversation_card,
)


def emit_conversation_updated(conversation_id: int):
    """
    Broadcast the latest state of a conversation to every participant.

    Call this whenever the conversation changes:
    - new message
    - edit
    - delete
    - forward
    - reactions (future)
    """

    conversation = Conversation.query.get(conversation_id)

    if not conversation:
        return

    for participant in conversation.participants:

        card = build_conversation_card(
            conversation,
            participant.user_id,
        )

        if not card:
            continue

        socketio.emit(
            "conversation:updated",
            card,
            room=f"user_{participant.user_id}",
        )