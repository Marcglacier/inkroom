# app/inbox/services/inbox/get_inbox.py

from app.inbox.models.conversation import Conversation
from app.inbox.models.conversation_participant import ConversationParticipant
from app.inbox.models.conversation_clear import ConversationClear
from app.inbox.models.message import Message
from app.models.user import User


def get_inbox(user_id):

    # --------------------------------
    # GET UNIQUE CONVERSATIONS
    # --------------------------------
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

        # --------------------------------
        # GET PARTICIPANTS
        # --------------------------------
        participants = ConversationParticipant.query.filter_by(
            conversation_id=convo.id
        ).all()

        participant_ids = [x.user_id for x in participants]

        # --------------------------------
        # DETECT SAVED MESSAGES
        # --------------------------------
        if len(set(participant_ids)) == 1:

            other_user_id = user_id
            username = "Saved Messages"

        else:

            other = ConversationParticipant.query.filter(
                ConversationParticipant.conversation_id == convo.id,
                ConversationParticipant.user_id != user_id
            ).first()

            if not other:
                continue

            other_user = User.query.get(other.user_id)
            if not other_user:
                continue

            other_user_id = other_user.id
            username = other_user.username

        # --------------------------------
        # CHECK IF USER CLEARED CHAT
        # --------------------------------
        clear = ConversationClear.query.filter_by(
            conversation_id=convo.id,
            user_id=user_id
        ).first()

        query = Message.query.filter(
            Message.conversation_id == convo.id,
            Message.deleted_for_everyone.is_(False)
        )

        if clear:
            query = query.filter(
                Message.created_at > clear.cleared_at
            )

        # --------------------------------
        # LAST MESSAGE
        # --------------------------------
        last_msg = query.order_by(
            Message.created_at.desc()
        ).first()

        # --------------------------------
        # UNREAD COUNT
        # --------------------------------
        unread_query = Message.query.filter(
            Message.conversation_id == convo.id,
            Message.sender_id != user_id,
            Message.read_at.is_(None),
            Message.deleted_for_everyone.is_(False)
        )

        if clear:
            unread_query = unread_query.filter(
                Message.created_at > clear.cleared_at
            )

        unread_count = unread_query.count()

        # --------------------------------
        # HIDE CONVERSATION IF EMPTY
        # --------------------------------
        if not last_msg:
            continue

        results.append({
            "conversation_id": convo.id,
            "user_id": other_user_id,
            "username": username,
            "last_message": last_msg.content,
            "unread": unread_count
        })

    return results