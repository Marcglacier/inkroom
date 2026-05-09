# app/inbox/sockets/connect_events.py
from flask_socketio import disconnect
from flask_jwt_extended import decode_token
from flask import request
from datetime import datetime

from app.extensions import db
from app.models.user import User


def register_connect_events(socketio):

    # =========================
    # CONNECT
    # =========================
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

            user = User.query.get(user_id)

            if user:
                user.online = True
                db.session.commit()

            print(f"✅ User {user_id} connected to socket")

        except Exception as e:
            print("❌ Socket auth failed:", str(e))
            disconnect()


    # =========================
    # DISCONNECT
    # =========================
    @socketio.on("disconnect")
    def disconnect_event():

        token = request.args.get("token")

        if not token:
            return

        try:
            decoded = decode_token(token)
            user_id = int(decoded["sub"])

            user = User.query.get(user_id)

            if user:
                user.online = False
                user.last_seen = datetime.utcnow()
                db.session.commit()

            print(f"👋 User {user_id} disconnected")

        except Exception as e:
            print("⚠️ Disconnect error:", str(e))