from flask_socketio import emit

online_users = {}


def register_presence_events(socketio):

    @socketio.on("presence:ping")
    def handle_ping(data):
        user_id = data.get("user_id")

        if not user_id:
            return

        online_users[user_id] = True

        emit("presence:pong", {
            "user_id": user_id,
            "status": "online"
        }, broadcast=True)


    @socketio.on("presence:check")
    def handle_check(data):
        user_id = data.get("user_id")

        emit("presence:status", {
            "user_id": user_id,
            "online": user_id in online_users
        })