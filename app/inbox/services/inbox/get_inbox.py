# app/inbox/services/inbox/get_inbox.py
from sqlalchemy import distinct
from app.extensions import db
from app.inbox.models import Conversation, ConversationParticipant
from app.inbox.services.conversations.core.conversation_builder import ConversationCardBuilder
from app.inbox.models.conversations.conversation_hide import ConversationHide
from app.inbox.models.conversations.conversation_archive import ( ConversationArchive, )
from app.models.settings.user_restriction import UserRestriction

def get_inbox(user_id):

    convo_ids = [
        c[0]
        for c in (
            db.session.query(
                distinct(ConversationParticipant.conversation_id)
            )
            .filter(ConversationParticipant.user_id == user_id)
            .all()
        )
    ]

    results = []

    for convo_id in convo_ids:



        convo = Conversation.query.get(convo_id)
        if not convo:
            continue
        # Restricted chats leave this user's normal inbox.
        # The other participant's inbox remains unchanged.
        if convo.status == "active":
            participants = ConversationParticipant.query.filter_by(
                conversation_id=convo_id
            ).all()

            other_user_ids = [
                participant.user_id
                for participant in participants
                if participant.user_id is not None
                and participant.user_id != user_id
            ]

            if len(other_user_ids) == 1:
                restricted = UserRestriction.query.filter_by(
                    restricter_id=user_id,
                    restricted_id=other_user_ids[0],
                ).first()

                if restricted:
                    continue
        # check hidden before building card
        hidden = ConversationHide.query.filter_by(
            conversation_id=convo_id, user_id=user_id
        ).first()
        if hidden:
            continue

        archived = ConversationArchive.query.filter_by(
            conversation_id=convo_id, user_id=user_id,).first()

        if archived:
            continue

        card = ConversationCardBuilder(convo, user_id).build()
        if not card:
            continue

        results.append(card)

    # sort once, after building
    results.sort(
        key=lambda c: (
            c["is_pinned"],
            c["last_message"]["created_at"]
            if c["last_message"]  else "",
        ),
        reverse=True,
    )

    return results