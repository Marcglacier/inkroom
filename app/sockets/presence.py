from flask_socketio import emit
from flask import request
from datetime import datetime, timezone


online_users = {}
last_seen = {}
user_sockets = {}


def register_presence_events(socketio):


    @socketio.on("presence:ping")
    def handle_ping(data):

        print(
            "🫀 PING RECEIVED",
            data
        )

        user_id = data.get("user_id")

        if not user_id:
            return

        user_id = int(user_id)

        online_users[user_id] = True
        user_sockets[request.sid] = user_id

        print(
            "🧠 USER SOCKETS:",
            user_sockets
        )

        print(
            "🟢 ONLINE USERS:",
            online_users
        )

        emit(
            "presence:status",
            {
                "user_id": user_id,
                "online": True
            },
            broadcast=True
        )


    @socketio.on("disconnect")
    def handle_disconnect():

        print(
            "🔴 SOCKET LEFT",
            request.sid
        )

        print(
            "🧠 USER SOCKETS BEFORE:",
            user_sockets
        )

        user_id = user_sockets.pop(
            request.sid,
            None
        )

        print(
            "🧠 USER SOCKETS AFTER:",
            user_sockets
        )

        if not user_id:
            return

        online_users[user_id] = False

        print(
            "🟢 ONLINE USERS AFTER DISCONNECT:",
            online_users
        )

        last_seen[user_id] = datetime.now(
            timezone.utc
        ).isoformat()

        print(
            "🔴 USER OFFLINE:",
            user_id
        )

        emit(
            "presence:status",
            {
                "user_id": user_id,
                "online": False,
                "last_seen": last_seen[user_id]
            },
            broadcast=True
        )


    @socketio.on("presence:check")
    def handle_check(data):

        user_id = data.get("user_id")

        if not user_id:
            return

        user_id = int(user_id)

        print(
            "👀 PRESENCE CHECK:",
            user_id
        )

        print(
            "📦 ONLINE USERS:",
            online_users
        )

        print(
            "📦 LAST SEEN:",
            last_seen
        )

        emit(
            "presence:status",
            {
                "user_id": user_id,
                "online": online_users.get(
                    user_id,
                    False
                ),
                "last_seen": last_seen.get(
                    user_id
                )
            }
        )