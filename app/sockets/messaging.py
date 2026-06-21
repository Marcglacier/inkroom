from flask_socketio import emit, join_room

active_chambers = {}


def register_messaging_events(socketio):

    @socketio.on("connect")
    def connected():

        print(
            "🟢 SOCKET CONNECTED"
        )

    @socketio.on("message:join")
    def join_chat(data):

        print(
            "🔥 JOIN REQUEST RECEIVED:",
            data
        )

        conversation_id = data.get(
            "conversation_id"
        )

        user_id = data.get(
            "user_id"
        )

        if not conversation_id:
            return

        if user_id:

            active_chambers[
                int(user_id)
            ] = int(conversation_id)

            print(
                "👁 ACTIVE CHAMBERS:",
                active_chambers
            )

        room = f"conversation_{conversation_id}"

        join_room(room)

        print(
            "🔥 USER JOINED ROOM:",
            room
        )

        emit(
            "room:joined",
            {
                "room": room
            }
        )