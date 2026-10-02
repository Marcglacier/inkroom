from flask_socketio import join_room, emit
from flask_jwt_extended import decode_token
from flask import current_app, request
from .presence_store import (
    set_online, set_offline_later, online_users, last_seen, has_other_connections
    )
from app.sockets.messaging import active_chambers, sid_to_user
from app.extensions import db
from app.inbox.models.messages.message import Message
from app.inbox.models.conversations.conversation_participant import ConversationParticipant
from app.inbox.services.presence.presence_events import (emit_presence_status,)
from app.inbox.services.calls.marks.mark_user_calls_disconnected import (
    MarkUserCallsDisconnected,
)
from app.inbox.services.calls.marks.mark_user_calls_reconnected import (
    MarkUserCallsReconnected,
)


def register_connection_events(socketio):

    @socketio.on("connect")
    def handle_connect(auth):
        print("\n🔥 SOCKET CONNECT ATTEMPT", "AUTH:", auth)

        token = auth.get("token") if isinstance(auth, dict) else None
        if not token:
            print("❌ NO TOKEN")
            return False

        try:
            decoded = decode_token(token)
            user_id = int(decoded["sub"])
            MarkUserCallsReconnected(user_id).execute()
            set_online(user_id, request.sid)

            # Mark "sent" messages as "delivered"
            conversation_ids = [p.conversation_id for p in ConversationParticipant.query.filter_by(user_id=user_id).all()]
            messages = Message.query.filter(
                Message.conversation_id.in_(conversation_ids),
                Message.sender_id != user_id,
                Message.status == "sent"
            ).all()

            print("📦 SENT MESSAGES FOUND:", len(messages))
            for msg in messages:
                msg.status = "delivered"
                socketio.emit("message:status", {"message_id": msg.id, "status": "delivered"}, room=f"user_{msg.sender_id}")
                print("📦 DELIVERED:", msg.id)
            db.session.commit()

            # Join rooms
            join_room(f"user_{user_id}")
            join_room("global_feed")

            print("🟢 CONNECT ONLINE:", user_id, "ONLINE:", online_users)

            # Emit presence updates
            emit_presence_status(
                user_id=user_id,
                online=True,)

            print("📦 SENDING ONLINE SNAPSHOT")
            for uid, status in online_users.items():
                emit("presence:status", {"user_id": uid, "online": status, "last_seen": last_seen.get(uid)})

            print("✅ CONNECT COMPLETE")
            return True

        except Exception as e:
            print("❌ SOCKET AUTH ERROR", e)
            return False

    @socketio.on("presence:request")
    def presence_request():
        print("📡 PRESENCE SNAPSHOT REQUEST")
        for uid, status in online_users.items():
            emit("presence:status", {"user_id": uid, "online": status, "last_seen": last_seen.get(uid)})

    @socketio.on("disconnect")
    def handle_disconnect():
        print("\n🔥🔥 SOCKET DISCONNECTED", "SID:", request.sid)

        # Remove active chat
        user_id = sid_to_user.pop(request.sid, None)
        if user_id:
            active_chambers.pop(user_id, None)
            print("🧹 REMOVED CHAT USER:", user_id)

        # If user has other connections, don't mark offline
        if user_id and not has_other_connections(user_id, request.sid):
            MarkUserCallsDisconnected(user_id).execute()

        # Start offline timer
        set_offline_later(
            request.sid,
            lambda uid:
                emit_presence_status(
                    user_id=uid,
                    online=False,
                    last_seen=last_seen.get(uid),
                ),
        )
        print("⏳ OFFLINE TIMER STARTED")
