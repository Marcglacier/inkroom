# app/inbox/services/conversations/delete_conversation.py
from app.extensions import db
from app.inbox.models.conversation_hide import ConversationHide


def delete_conversation(conversation_id, user_id):

    hidden = ConversationHide(
        conversation_id=conversation_id,
        user_id=user_id
    )

    db.session.add(hidden)
    db.session.commit()

    return {
        "conversation_id": conversation_id,
        "status": "deleted_from_inbox"
    }