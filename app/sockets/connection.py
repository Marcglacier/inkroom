from flask_socketio import join_room, disconnect
from flask_jwt_extended import decode_token
from flask import request

from app.extensions import db
from app.models.user import User


def register_connection_events(socketio):

    @socketio.on("connect")
    def handle_connect(auth):

        token = None

        if auth and isinstance(auth, dict):
            token = auth.get("token")

        if not token:
            print("❌ Socket rejected: missing token")
            return False

        try:
            decoded = decode_token(token)
            user_id = int(decoded["sub"])

            join_room(f"user_{user_id}")

            user = User.query.get(user_id)
            if user:
                user.online = True
                db.session.commit()

            print(f"✅ CONNECTED: user {user_id}")

            return True

        except Exception as e:
            print("❌ Socket auth failed:", e)
            return False


    @socketio.on("disconnect")
    def handle_disconnect():

        token = request.args.get("token")

        if not token:
            return

        try:
            decoded = decode_token(token)
            user_id = int(decoded["sub"])

            user = User.query.get(user_id)
            if user:
                user.online = False
                db.session.commit()

            print(f"👋 DISCONNECTED: user {user_id}")

        except Exception as e:
            print("disconnect error:", e)