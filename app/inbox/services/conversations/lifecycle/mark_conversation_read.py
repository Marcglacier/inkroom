from app.extensions import db
from app.inbox.models import Message
from app.inbox.services.conversations.core.conversation_events import ( emit_conversation_updated, )
from app.extensions import db, socketio
from app.inbox.services.conversations.core.conversation_guard import ( ConversationGuard, )

def mark_conversation_read(conversation_id, user_id):

    participant = ConversationGuard.require_participant(
        conversation_id, user_id,
    )

    # mark messages as read
    messages = (
        Message.query.filter(
            Message.conversation_id == conversation_id,
            Message.sender_id != user_id,
            Message.read_at.is_(None),
        ).all()
    )
    Message.query.filter(
        Message.conversation_id == conversation_id,
        Message.sender_id != user_id,
        Message.read_at.is_(None),
    ).update(
        {
            "read_at": db.func.now(),
            "status": "read",
        },
        synchronize_session=False
    )


    # update last read pointer
    
    print("========== MARK READ ==========")
    print("conversation:", conversation_id)
    print("user:", user_id)
    print( "BEFORE:", participant.last_read_message_id)
       
    last_message = (
        Message.query
        .filter_by(conversation_id=conversation_id)
        .order_by(Message.id.desc())
        .first()
    )


    if participant and last_message:
        participant.last_read_message_id = last_message.id
        print("AFTER:", participant.last_read_message_id)


    db.session.commit()
    print("COMMITTING LAST READ", participant.last_read_message_id)
    for message in messages:
        socketio.emit(
            "message:status",
            {
                "conversation_id": conversation_id,
                "message_id": message.id,
                "status": "read",
            },
            room=f"conversation_{conversation_id}",
        )
    last_read_id = participant.last_read_message_id if participant else None

    socketio.emit(
         "conversation:read",
             {
                "conversation_id": conversation_id,
                "user_id": user_id,
                "last_read_message_id": last_read_id,
            },
             room=f"user_{user_id}",
        )
    emit_conversation_updated(conversation_id)