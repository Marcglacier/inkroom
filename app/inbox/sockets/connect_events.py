# app/inbox/sockets/connect_events.py

from flask_socketio import disconnect
from flask_jwt_extended import decode_token
from flask import request


def register_connect_events(socketio):

    @socketio.on("connect")
    def connect():

        token = request.args.get("token")

        if not token:
            print("❌ Socket connection rejected: no token")
            disconnect()
            return

        try:
            decoded = decode_token(token)
            user_id = int(decoded["sub"])

            print(f"✅ User {user_id} connected to socket")

        except Exception as e:
            print("❌ Socket auth failed:", str(e))
            disconnect()