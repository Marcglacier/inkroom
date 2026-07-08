from flask_socketio import emit, join_room
from flask import request
from app.sockets.messaging import sid_to_user
from app.inbox.models.conversation_participant import ConversationParticipant


def register_typing_events(socketio):

    @socketio.on("join_conversation")
    def join_conversation(data):
        cid = data.get("conversation_id")
        if cid:
            join_room(f"conversation_{cid}")

    @socketio.on("typing_start")
    def typing_start(data):
        uid = sid_to_user.get(request.sid)
        cid = data.get("conversation_id")

        if not uid or not cid:
            return

        payload = {
            "user_id": uid,
            "conversation_id": cid,
        }

        # Users inside the conversation
        emit(
            "user:typing",
            payload,
            room=f"conversation_{cid}",
            include_self=False,
        )

        # Users outside the conversation (Raven Hall)
        participants = ConversationParticipant.query.filter_by(
            conversation_id=cid
        ).all()

        for participant in participants:
            if participant.user_id == uid:
                continue

            socketio.emit(
                "user:typing",
                payload,
                room=f"user_{participant.user_id}",
            )

    @socketio.on("typing_stop")
    def typing_stop(data):
        uid = sid_to_user.get(request.sid)
        cid = data.get("conversation_id")

        if not uid or not cid:
            return

        payload = {
            "user_id": uid,
            "conversation_id": cid,
        }

        emit(
            "user:stop_typing",
            payload,
            room=f"conversation_{cid}",
            include_self=False,
        )

        participants = ConversationParticipant.query.filter_by(
            conversation_id=cid
        ).all()

        for participant in participants:
            if participant.user_id == uid:
                continue

            socketio.emit(
                "user:stop_typing",
                payload,
                room=f"user_{participant.user_id}",
            )