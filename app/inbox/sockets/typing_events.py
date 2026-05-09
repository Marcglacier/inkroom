# app/inbox/sockets/typing_events.py

from flask_socketio import emit, join_room
from flask_jwt_extended import decode_token
from flask import request


def register_typing_events(socketio):

    # =========================
    # SOCKET CONNECT
    # =========================
    @socketio.on("connect")
    def handle_connect():

        token = request.args.get("token")

        if not token:
            return False

        try:
            decoded = decode_token(token)
            user_id = int(decoded["sub"])

            join_room(f"user_{user_id}")

            print(f"User {user_id} connected")

        except Exception:
            return False


    # =========================
    # JOIN CONVERSATION ROOM
    # =========================
    @socketio.on("join_conversation")
    def join_conversation(data):

        conversation_id = data.get("conversation_id")

        if not conversation_id:
            return

        join_room(f"conversation_{conversation_id}")

        print(f"User joined conversation {conversation_id}")


    # =========================
    # USER STARTS TYPING
    # =========================
    @socketio.on("typing_start")
    def typing_start(data):

        token = request.args.get("token")
        decoded = decode_token(token)
        user_id = int(decoded["sub"])

        conversation_id = data.get("conversation_id")

        emit(
            "user_typing",
            {
                "user_id": user_id,
                "conversation_id": conversation_id
            },
            room=f"conversation_{conversation_id}",
            include_self=False
        )


    # =========================
    # USER STOPS TYPING
    # =========================
    @socketio.on("typing_stop")
    def typing_stop(data):

        token = request.args.get("token")
        decoded = decode_token(token)
        user_id = int(decoded["sub"])

        conversation_id = data.get("conversation_id")

        emit(
            "user_stop_typing",
            {
                "user_id": user_id,
                "conversation_id": conversation_id
            },
            room=f"conversation_{conversation_id}",
            include_self=False
        )