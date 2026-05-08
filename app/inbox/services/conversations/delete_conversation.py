# app/inbox/services/conversations/delete_conversation.py

from datetime import datetime
from app.extensions import db
from app.inbox.models.conversation_clear import ConversationClear


def delete_conversation(conversation_id, user_id):

    clear = ConversationClear.query.filter_by(
        conversation_id=conversation_id,
        user_id=user_id
    ).first()

    if not clear:
        clear = ConversationClear(
            conversation_id=conversation_id,
            user_id=user_id,
            cleared_at=datetime.utcnow()
        )
        db.session.add(clear)
    else:
        clear.cleared_at = datetime.utcnow()

    db.session.commit()

    return {
        "conversation_id": conversation_id,
        "status": "cleared"
    }