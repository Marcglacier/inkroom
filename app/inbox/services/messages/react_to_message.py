
from datetime import datetime
from app.inbox.services.settings.blocks.block_policy import BlockPolicy
from app.extensions import db, socketio
from app.inbox.models.messages.message import Message
from app.inbox.models.messages.message_reaction import MessageReaction
from app.inbox.models.conversations.conversation import Conversation
from app.inbox.models.conversations.conversation_participant import (
    ConversationParticipant,
)
from app.inbox.services.messages.message_reaction_aggregator import (
    build_reactions,
)
from app.inbox.services.messages.create_system_message import (
    create_system_message,
)
from app.inbox.serializers.message_serializer import MessageSerializer
from app.inbox.services.conversations.core.conversation_events import (
    emit_conversation_updated,
)

def toggle_reaction(user_id, message_id, emoji):
    message = Message.query.get(message_id)

    if not message:
        return {"error": "Message not found"}, 404

    convo = Conversation.query.get(message.conversation_id)

    if not convo:
        return {"error": "Conversation not found"}, 404

    participant = ConversationParticipant.query.filter_by(
        conversation_id=convo.id,
        user_id=user_id,
    ).first()

    if not participant:
        return {"error": "You cannot react to this conversation"}, 403

    if BlockPolicy.blocks_either_user(user_id, message.sender_id):
        return {"error": "Reactions are unavailable"}, 403

    existing = MessageReaction.query.filter_by(
        user_id=user_id,
        message_id=message_id,
    ).first()

    if not existing:
        reaction = MessageReaction(
            user_id=user_id,
            message_id=message_id,
            reaction=emoji,
            created_at=datetime.utcnow(),
        )
        db.session.add(reaction)
        status = "added"

    elif existing.reaction == emoji:
        db.session.delete(existing)
        status = "removed"

    else:
        existing.reaction = emoji
        status = "replaced"

    db.session.commit()

    system = create_system_message(
        conversation_id=convo.id,
        sender_id=user_id,
        event=f"message_reaction_{status}",
        target_message_id=message.id,
        content=emoji if status != "removed" else None,
    )
    db.session.commit()

    socketio.emit(
        "message:reaction",
        {
            "message_id": message.id,
            "conversation_id": convo.id,
            "reactions": build_reactions(message.id),
        },
        room=f"conversation_{convo.id}",
    )

    socketio.emit(
        "message:new",
        MessageSerializer(system).to_dict(),
        room=f"conversation_{convo.id}",
    )
    emit_conversation_updated(convo.id)

    return {
        "status": status,
        "emoji": emoji,
    }
