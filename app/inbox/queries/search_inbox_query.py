# app/inbox/queries/search_inbox_query.py
from sqlalchemy import or_

from app.inbox.models.messages.message import Message
from app.inbox.models.conversations.conversation_participant import ConversationParticipant
from app.inbox.models.conversations.conversation_clear import ConversationClear
from app.models.user import User
from app.storage.service import get_file_url



def search_inbox_messages(user_id, text):

    if not text or not text.strip():
        return []


    text = text.strip()



    results = []



    # =========================
    # 1. SEARCH USERS
    # =========================


    users = (
        User.query
        .filter(
            User.id != user_id,
            or_(
                User.username.ilike(f"%{text}%"),
                User.name.ilike(f"%{text}%")
            )
        )
        .limit(20)
        .all()
    )


    for user in users:


        results.append({

            "type":"user",

            "user_id":user.id,

            "name":user.name,

            "username":user.username,

            "avatar":(get_file_url(user.profile_picture)
                       if user.profile_picture else None)

        })



    # =========================
    # 2. SEARCH MESSAGES
    # =========================


    last_clear_subq = (
        ConversationClear.query
        .filter(
            ConversationClear.user_id == user_id,
            ConversationClear.conversation_id == Message.conversation_id
        )
        .order_by(
            ConversationClear.cleared_at.desc()
        )
        .limit(1)
        .with_entities(
            ConversationClear.cleared_at
        )
        .scalar_subquery()
    )



    messages = (
        Message.query

        .join(
            ConversationParticipant,
            ConversationParticipant.conversation_id ==
            Message.conversation_id
        )

        .filter(

            ConversationParticipant.user_id == user_id,

            Message.deleted_for_everyone == False,

            Message.content.ilike(
                f"%{text}%"
            ),

            or_(
                last_clear_subq.is_(None),
                Message.created_at > last_clear_subq
            )

        )

        .order_by(
            Message.created_at.desc()
        )

        .limit(20)

        .all()
    )



    for msg in messages:


        results.append({

            "type":"message",

            "message_id":msg.id,

            "conversation_id":
                msg.conversation_id,

            "content":
                msg.content,

            "sender_id":
                msg.sender_id,

            "created_at":
                msg.created_at

        })



    return results