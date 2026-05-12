# app/inbox/queries/search_inbox_query.py
from sqlalchemy import or_
from app.inbox.models.message import Message
from app.inbox.models.conversation_participant import ConversationParticipant
from app.inbox.models.conversation_clear import ConversationClear
from app.models.user import User


def search_inbox_messages(user_id, text):
    if not text or not text.strip():
        return []

    text = text.strip()

    last_clear_subq = (
        ConversationClear.query
        .filter(
            ConversationClear.user_id == user_id,
            ConversationClear.conversation_id == Message.conversation_id
        )
        .order_by(ConversationClear.cleared_at.desc())
        .limit(1)
        .with_entities(ConversationClear.cleared_at)
        .scalar_subquery()
    )

    query = (
        Message.query
        .join(
            ConversationParticipant,
            ConversationParticipant.conversation_id == Message.conversation_id
        )
        .join(User, User.id == Message.sender_id)
        .filter(
            ConversationParticipant.user_id == user_id,
            Message.deleted_for_everyone == False,
            or_(
                Message.content.ilike(f"%{text}%"),
                User.username.ilike(f"%{text}%")
            ),
            or_(
                last_clear_subq.is_(None),
                Message.created_at > last_clear_subq
            )
        )
        .order_by(Message.created_at.desc())
        .limit(50)
    )

    return query.all()