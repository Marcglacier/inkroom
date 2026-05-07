# app/inbox/services/inbox/get_inbox.py

from app.inbox.models.conversation import Conversation
from app.inbox.models.conversation_participant import ConversationParticipant
from app.inbox.models.conversation_clear import ConversationClear
from app.inbox.models.conversation_hide import ConversationHide
from app.inbox.models.message import Message
from app.models.user import User


def get_inbox(user_id):

    convos = (
        ConversationParticipant.query
        .filter_by(user_id=user_id)
        .distinct(ConversationParticipant.conversation_id)
        .all()
    )

    results = []

    for p in convos:

        convo = Conversation.query.get(p.conversation_id)
        if not convo:
            continue

        if ConversationHide.query.filter_by(
            conversation_id=convo.id,
            user_id=user_id
        ).first():
            continue

        participants = ConversationParticipant.query.filter_by(
            conversation_id=convo.id
        ).all()

        ids = [x.user_id for x in participants]

        if len(set(ids)) == 1:
            other_user_id = user_id
            username = "Saved Messages"
        else:
            other = ConversationParticipant.query.filter(
                ConversationParticipant.conversation_id == convo.id,
                ConversationParticipant.user_id != user_id
            ).first()

            if not other:
                continue

            user = User.query.get(other.user_id)
            if not user:
                continue

            other_user_id = user.id
            username = user.username

        clear = ConversationClear.query.filter_by(
            conversation_id=convo.id,
            user_id=user_id
        ).first()

        base_query = Message.query.filter(
            Message.conversation_id == convo.id,
            Message.deleted_for_everyone.is_(False)
        )

        if clear:
            base_query = base_query.filter(
                Message.created_at > clear.cleared_at
            )

        last_msg = base_query.order_by(Message.created_at.desc()).first()
        if not last_msg:
            continue

        unread = Message.query.filter(
            Message.conversation_id == convo.id,
            Message.sender_id != user_id,
            Message.read_at.is_(None),
            Message.deleted_for_everyone.is_(False)
        )

        if clear:
            unread = unread.filter(
                Message.created_at > clear.cleared_at
            )

        results.append({
            "conversation_id": convo.id,
            "user_id": other_user_id,
            "username": username,
            "last_message": last_msg.content,
            "unread": unread.count()
        })

    return results