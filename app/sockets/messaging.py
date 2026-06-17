from flask_socketio import emit, join_room
from flask_jwt_extended import decode_token


def register_messaging_events(socketio):

    # =========================
    # JOIN CHAT ROOM
    # =========================
    @socketio.on("message:join")
    def join_chat(data):

        conversation_id = data.get("conversation_id")

        if not conversation_id:
            return

        room = f"conversation_{conversation_id}"
        join_room(room)

        print(f"💬 Joined chat room: {room}")


    # =========================
    # SEND MESSAGE
    # =========================
    @socketio.on("message:send")
    def send_message(data):

        conversation_id = data.get("conversation_id")

        if not conversation_id:
            return

        emit(
            "message:new",
            {
                "conversation_id": conversation_id,
                "sender_id": data.get("sender_id"),
                "content": data.get("content"),
            },
            room=f"conversation_{conversation_id}"
        )