from flask_socketio import join_room, leave_room
from flask_jwt_extended import decode_token
from flask import request

from app.extensions import db
from app.models.user import User


def register_connection_events(socketio):

    # =========================
    # CONNECT
    # =========================
    @socketio.on("connect")
    def handle_connect(auth):

        token = None

        if auth and isinstance(auth, dict):
            token = auth.get("token")

        if not token:
            print("❌ SOCKET REJECTED: missing token")
            return False

        try:
            decoded = decode_token(token)
            user_id = int(decoded["sub"])

            user_room = f"user_{user_id}"

            join_room(user_room)
            join_room("global_feed")

            user = User.query.get(user_id)
            if user:
                user.online = True
                db.session.commit()

            print("\n")
            print("🟢 SOCKET CONNECTED")
            print("sid:", request.sid)
            print("user_id:", user_id)
            print("joined room:", user_room)
            print("joined room: global_feed")
            print("\n")

            socketio.emit(
                "presence:update",
                {
                    "userId": user_id,
                    "online": True
                },
                room=user_room
            )

            return True

        except Exception as e:
            print("❌ SOCKET AUTH FAILED")
            print(e)
            return False

    # =========================
    # DISCONNECT
    # =========================
    @socketio.on("disconnect")
    def handle_disconnect():

        print("\n")
        print("👋 SOCKET DISCONNECTED")
        print("sid:", request.sid)
        print("\n")

        # optional:
        # don't try decoding token here
        # Socket.IO disconnect events don't reliably
        # have access to the original auth payload

        return