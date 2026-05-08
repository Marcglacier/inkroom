from sqlalchemy import distinct

from app.extensions import db
from app.inbox.models.conversation import Conversation
from app.inbox.models.conversation_participant import ConversationParticipant
from app.inbox.models.conversation_clear import ConversationClear
from app.inbox.models.message import Message
from app.models.user import User
from app.inbox.services.messages.message_reaction_aggregator import build_reactions

def get_inbox(user_id):

    print("\n========== INBOX DEBUG START ==========")
    print(f"USER ID: {user_id}")

    convo_ids = db.session.query(
        distinct(ConversationParticipant.conversation_id)
    ).filter(
        ConversationParticipant.user_id == user_id
    ).all()

    convo_ids = [c[0] for c in convo_ids]
    results = []

    for convo_id in convo_ids:

        convo = Conversation.query.get(convo_id)
        if not convo:
            continue

        participants = ConversationParticipant.query.filter_by(
            conversation_id=convo_id
        ).all()

        if not participants:
            continue

        participant_ids = [p.user_id for p in participants]

        # =========================
        # SELF CHAT
        # =========================
        is_self = len(participant_ids) == 1 and participant_ids[0] == user_id

        if is_self:
            other_user_id = user_id
            username = "Saved Messages"
        else:
            other = next((p for p in participants if p.user_id != user_id), None)
            if not other:
                continue

            user = User.query.get(other.user_id)
            if not user:
                continue

            other_user_id = user.id
            username = user.username

        # =========================
        # CLEAR LOGIC
        # =========================
        clear = ConversationClear.query.filter_by(
            conversation_id=convo_id,
            user_id=user_id
        ).first()

        msg_query = Message.query.filter(
            Message.conversation_id == convo_id,
            Message.deleted_for_everyone.is_(False)
        )

        if clear:
            msg_query = msg_query.filter(
                Message.created_at > clear.cleared_at
            )

        last_msg = msg_query.order_by(
            Message.created_at.desc()
        ).first()

        if not last_msg:
            continue

        # =========================
        # UNREAD COUNT
        # =========================
        unread_query = Message.query.filter(
            Message.conversation_id == convo_id,
            Message.sender_id != user_id,
            Message.read_at.is_(None),
            Message.deleted_for_everyone.is_(False)
        )

        if clear:
            unread_query = unread_query.filter(
                Message.created_at > clear.cleared_at
            )

        # =========================
        # REPLY PREVIEW
        # =========================
        reply_data = None
        if last_msg.reply_to:
            reply_data = {
                "id": last_msg.reply_to.id,
                "content": last_msg.reply_to.content,
                "sender_username": (
                    last_msg.reply_to.sender.username
                    if last_msg.reply_to.sender else None
                )
            }

        results.append({
            "conversation_id": convo_id,
            "user_id": other_user_id,
            "username": username,

            "last_message": {
                "id": last_msg.id,
                "content": last_msg.content,
                "sender_id": last_msg.sender_id,
                "sender_username": (
                    last_msg.sender.username if last_msg.sender else None
                ),
                "created_at": last_msg.created_at.isoformat(),
                "reply_to": reply_data,
                "reactions": build_reactions(last_msg.id)
            },

            "unread": unread_query.count()
        })

    print("\n========== INBOX DEBUG END ==========\n")
    return results