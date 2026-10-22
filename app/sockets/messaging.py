from flask_socketio import emit, join_room, leave_room
from flask import request
from app.extensions import db
from app.inbox.models.messages.message import Message
from app.inbox.models.conversations.conversation_participant import ConversationParticipant
from app.sockets.calls.helpers.authenticate_socket import (
    get_authenticated_socket_user,
)
from app.inbox.services.settings.blocks.block_policy import BlockPolicy

active_chambers = {}
sid_to_user = {}

def register_messaging_events(socketio):
    @socketio.on("message:join")
    def join_chat(data):
        print("🔥 JOIN REQUEST RECEIVED:", data)
        print("🚨 JOIN HANDLER CALLED SID:", request.sid)
        print("🚨 DATA:", data)
        conversation_id = (data or {}).get("conversation_id")
        user_id = get_authenticated_socket_user()

        if user_id is None:
            return {"ok": False, "error": "Socket is not authenticated."}

        if not conversation_id:
            return {"ok": False, "error": "conversation_id is required."}

        try:
            conversation_id = int(conversation_id)
        except (TypeError, ValueError):
            return {"ok": False, "error": "Invalid conversation_id."}
        if not conversation_id: return
        participant = ( ConversationParticipant.query
            .filter_by(  conversation_id=conversation_id,  user_id=user_id, )
            .first() )
        if not participant:
            print( f"❌ Unauthorized join attempt: " f"user={user_id}, conversation={conversation_id}")
            return
        other_participants = (
            ConversationParticipant.query
            .filter(
                ConversationParticipant.conversation_id == conversation_id,
                ConversationParticipant.user_id != user_id,
            )
            .all()
        )

        for other in other_participants:
            if BlockPolicy.blocks_either_user(
                user_id,
                other.user_id,
            ):
                return {
                    "ok": False,
                    "error": "Conversation access is unavailable.",
                }
        if user_id:
            active_chambers[int(user_id)] = int(conversation_id)
            sid_to_user[request.sid] = int(user_id)
            print("👁 ACTIVE CHAMBERS:", active_chambers)
        room = f"conversation_{conversation_id}"
        join_room(room)
        print("🔥 USER JOINED ROOM:", room)
        emit("room:joined", {"room": room})
        if user_id:
           active_chambers[int(user_id)] = int(conversation_id)
           sid_to_user[request.sid] = int(user_id)


    @socketio.on("message:leave")
    def leave_chat(data):
        print("🚪 LEAVE REQUEST RECEIVED:", data)
        user_id = get_authenticated_socket_user()
        conversation_id = (data or {}).get("conversation_id")

        if user_id is None:
            return {"ok": False, "error": "Socket is not authenticated."}
        if user_id: active_chambers.pop(int(user_id), None)
        if conversation_id: leave_room(f"conversation_{conversation_id}")
        print("🧹 ACTIVE CHAMBERS AFTER LEAVE:", active_chambers)

    @socketio.on("chamber:open")
    def chamber_open(data):
        user_id = get_authenticated_socket_user()
        conversation_id = (data or {}).get("conversation_id")

        if user_id is None or not conversation_id:
            return

        try:
            conversation_id = int(conversation_id)
        except (TypeError, ValueError):
            return

        participant = (
            ConversationParticipant.query
            .filter_by(
                conversation_id=conversation_id,
                user_id=user_id,
            )
            .first()
        )

        if participant is None:
            return

        active_chambers[user_id] = conversation_id


    @socketio.on("chamber:close")
    def chamber_close(_data):
        user_id = get_authenticated_socket_user()

        if user_id is None:
            return

        active_chambers.pop(user_id, None)

