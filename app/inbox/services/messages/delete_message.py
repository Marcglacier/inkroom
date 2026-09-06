# app/inbox/services/messages/delete_message.py
from app.extensions import db, socketio
from datetime import datetime
from app.inbox.serializers.message_serializer import MessageSerializer
from app.inbox.models.messages.pinned_message import PinnedMessage

def emit_delete(message):
    socketio.emit(
        "message:deleted",
        MessageSerializer(message).to_dict(),
        room=f"conversation_{message.conversation_id}",
    )


def delete_for_me(message, user_id):
    print(
     "BEFORE:", message.deleted_for_users
    )

    # Make a NEW list instead of mutating the existing one
    deleted_users = list(message.deleted_for_users or [])

    if user_id not in deleted_users:
        deleted_users.append(user_id)

    message.deleted_for_users = deleted_users

    db.session.commit()
    print(
     "AFTER:", message.deleted_for_users
    )

    print(
        "DELETE FOR ME:",
        message.id,
        message.deleted_for_users
    )

    emit_delete(message)


def delete_for_everyone(message):

    message.deleted_for_everyone = True
    message.delete_requested_at = datetime.utcnow()

    # Remove pin if this message is pinned
    pin = PinnedMessage.query.filter_by(
        message_id=message.id
    ).first()

    if pin:
        db.session.delete(pin)

    db.session.commit()

    emit_delete(message)

    if pin:
        socketio.emit(
            "message:unpinned",
            {
                "conversation_id": message.conversation_id,
                "message_id": message.id,
            },
            room=f"conversation_{message.conversation_id}",
        )

def undo_delete(message, user_id):

    message.deleted_for_everyone = False
    message.delete_requested_at = None

    deleted_users = message.deleted_for_users or []

    if user_id in deleted_users:
        deleted_users.remove(user_id)

    message.deleted_for_users = deleted_users

    db.session.commit()

    emit_delete(message)

    return message