
from flask_socketio import join_room
from flask import request

from app.sockets.messaging import sid_to_user
from app.inbox.models.conversations.conversation_participant import (
    ConversationParticipant,
)
from app.inbox.services.settings.blocks.block_policy import BlockPolicy


def register_typing_events(socketio):

    @socketio.on("join_conversation")
    def join_conversation(data):
        uid = sid_to_user.get(request.sid)
        cid = (data or {}).get("conversation_id")

        if not uid or not cid:
            return

        participant = ConversationParticipant.query.filter_by(
            conversation_id=cid,
            user_id=uid,
        ).first()

        if not participant:
            return

        others = ConversationParticipant.query.filter(
            ConversationParticipant.conversation_id == cid,
            ConversationParticipant.user_id != uid,
        ).all()

        for other in others:
            if other.user_id is None:
                continue

            if BlockPolicy.blocks_either_user(uid, other.user_id):
                return

        join_room(f"conversation_{cid}")

    def broadcast_typing(data, event):
        uid = sid_to_user.get(request.sid)
        cid = (data or {}).get("conversation_id")

        if not uid or not cid:
            return

        participant = ConversationParticipant.query.filter_by(
            conversation_id=cid,
            user_id=uid,
        ).first()

        if not participant:
            return

        others = ConversationParticipant.query.filter(
            ConversationParticipant.conversation_id == cid,
            ConversationParticipant.user_id != uid,
        ).all()

        payload = {
            "user_id": uid,
            "conversation_id": cid,
        }

        for other in others:
            target_id = other.user_id

            if target_id is None:
                continue

            if BlockPolicy.blocks_either_user(uid, target_id):
                continue

            socketio.emit(
                event,
                payload,
                room=f"user_{target_id}",
            )

    @socketio.on("typing_start")
    def typing_start(data):
        broadcast_typing(data, "user:typing")

    @socketio.on("typing_stop")
    def typing_stop(data):
        broadcast_typing(data, "user:stop_typing")
