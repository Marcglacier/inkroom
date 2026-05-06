# app/realtime/delivery.py
from datetime import datetime
from app.extensions import socketio, db
from app.inbox.models.message import Message


@socketio.on("message_received")
def handle_message_received(data):

    message_id = data["message_id"]

    msg = Message.query.get(message_id)

    if not msg or msg.delivered_at:
        return

    msg.delivered_at = datetime.utcnow()
    msg.status = "delivered"

    db.session.commit()

    socketio.emit(
        "message_delivered",
        {
            "message_id": message_id,
            "status": "delivered",
            "delivered_at": msg.delivered_at.isoformat()
        },
        room=f"user_{msg.sender_id}"
    )