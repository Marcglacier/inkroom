# app/inbox/services/messages/react_to_message.py
from datetime import datetime

from app.extensions import db, socketio
from app.inbox.models.message import Message
from app.inbox.models.message_reaction import MessageReaction
from app.inbox.models.conversation import Conversation
from app.inbox.models.conversation_participant import ConversationParticipant
from app.inbox.services.messages.message_reaction_aggregator import build_reactions



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

    def emit_update():
      socketio.emit(
          "message:reaction",
           {
              "message_id": message.id,
              "conversation_id": message.conversation_id,
              "reactions": build_reactions(message.id),
            },
           room=f"conversation_{message.conversation_id}",
        )

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

        emit_update()

        return {
            "status": "added",
            "emoji": emoji,
        }

    # =========================
    # REMOVE
    # =========================
    if existing.reaction == emoji:
        db.session.delete(existing)
        db.session.commit()

        emit_update()
        return {"status": "removed", "emoji": emoji}

    # =========================
    # REPLACE
    # =========================
    existing.reaction = emoji
    db.session.commit()

    emit_update()
    return {"status": "replaced", "emoji": emoji}