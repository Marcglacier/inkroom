# app/inbox/services/messages/react_to_message.py
from datetime import datetime

from app.extensions import db
from app.inbox.models.message import Message
from app.inbox.models.message_reaction import MessageReaction
from app.inbox.models.conversation import Conversation
from app.inbox.models.conversation_participant import ConversationParticipant


def toggle_reaction(user_id, message_id, emoji):

    # =========================
    # GET MESSAGE
    # =========================
    message = Message.query.get(message_id)

    if not message:
        return {"error": "Message not found"}, 404

    # =========================
    # GET CONVERSATION
    # =========================
    convo = Conversation.query.get(message.conversation_id)

    if not convo:
        return {"error": "Conversation not found"}, 404

    # =========================
    # CHECK PARTICIPATION
    # =========================
    participant = ConversationParticipant.query.filter_by(
        conversation_id=convo.id,
        user_id=user_id
    ).first()

    if not participant:
        return {"error": "You cannot react to this conversation"}, 403

    # =========================
    # CHECK EXISTING REACTION
    # =========================
    existing = MessageReaction.query.filter_by(
        user_id=user_id,
        message_id=message_id
    ).first()

    # =========================
    # ADD
    # =========================
    if not existing:
        reaction = MessageReaction(
            user_id=user_id,
            message_id=message_id,
            reaction=emoji,
            created_at=datetime.utcnow()
        )
        db.session.add(reaction)
        db.session.commit()

        return {"status": "added", "emoji": emoji}

    # =========================
    # REMOVE
    # =========================
    if existing.reaction == emoji:
        db.session.delete(existing)
        db.session.commit()

        return {"status": "removed", "emoji": emoji}

    # =========================
    # REPLACE
    # =========================
    existing.reaction = emoji
    db.session.commit()

    return {"status": "replaced", "emoji": emoji}