from flask_socketio import emit, join_room
from flask_jwt_extended import decode_token


def register_notification_events(socketio):

    # =========================
    # JOIN NOTIFICATION ROOM
    # =========================
    @socketio.on("notification:join")
    def join_notification_room(data):

        print("📡 [SOCKET] notification:join received:", data)

        token = data.get("token")

        if not token:
            print("❌ No token provided")
            return False

        try:
            decoded = decode_token(token)
            user_id = int(decoded["sub"])

            room = f"user_{user_id}"

            # 🔥 DEBUG LINES (IMPORTANT)
            print("👤 user_id decoded:", user_id)
            print("🏠 joining room:", room)

            join_room(room)

            print(f"🔔 Notification room joined: {room}")

            emit("notification:joined", {
                "room": room,
                "user_id": user_id
            })

        except Exception as e:
            print("❌ Notification join failed:", str(e))
            return False


    # =========================
    # PUSH NOTIFICATION HELPER
    # =========================
    def push_notification(user_id, payload):

        room = f"user_{user_id}"

        print("🚀 [SOCKET] PUSH NOTIFICATION")
        print("➡️ user_id:", user_id)
        print("🏠 room:", room)
        print("📦 payload:", payload)

        socketio.emit(
            "notification:new",
            payload,
            room=room
        )

        print("📡 EMIT COMPLETE ->", room)


    # expose helper globally
    socketio.push_notification = push_notification