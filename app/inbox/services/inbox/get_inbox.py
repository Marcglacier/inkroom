# app/inbox/services/inbox/get_inbox.py
from sqlalchemy import distinct
from app.extensions import db
from app.inbox.models import Conversation, ConversationParticipant, ConversationClear, ConversationRequest, Message
from app.models.user import User
from app.inbox.services.messages.message_reaction_aggregator import build_reactions

def get_inbox(user_id):
    print("\n========== GET INBOX ==========\nUSER:", user_id)

    convo_ids = [c[0] for c in db.session.query(distinct(ConversationParticipant.conversation_id))
                 .filter(ConversationParticipant.user_id == user_id).all()]
    results = []

    for convo_id in convo_ids:
        convo = Conversation.query.get(convo_id)
        if not convo: continue

        # hide pending requests from receiver
        if convo.status == "pending":
            req = ConversationRequest.query.filter_by(conversation_id=convo_id).first()
            if req and req.receiver_id == user_id: continue

        participants = ConversationParticipant.query.filter_by(conversation_id=convo_id).all()
        if not participants: continue

        if len(participants) == 1 and participants[0].user_id == user_id:
            other_user_id, username, name, avatar = user_id, "Saved Messages", "Saved Messages", None
        else:
            other = next((p for p in participants if p.user_id != user_id), None)
            if not other: continue
            user = User.query.get(other.user_id)
            if not user: continue
            other_user_id, username, name, avatar = user.id, user.username, user.name, user.profile_picture

        clear = ConversationClear.query.filter_by(conversation_id=convo_id, user_id=user_id).first()
        msg_query = Message.query.filter(Message.conversation_id == convo_id, Message.deleted_for_everyone.is_(False))
        if clear: msg_query = msg_query.filter(Message.created_at > clear.cleared_at)
        last_msg = msg_query.order_by(Message.created_at.desc()).first()
        if not last_msg: continue

        unread_query = Message.query.filter(
            Message.conversation_id == convo_id,
            Message.sender_id != user_id,
            Message.read_at.is_(None),
            Message.deleted_for_everyone.is_(False)
        )
        if clear: unread_query = unread_query.filter(Message.created_at > clear.cleared_at)

        results.append({
            "conversation_id": convo_id,
            "type": convo.type,
            "status": convo.status,
            "user_id": other_user_id,
            "username": username,
            "name": name,
            "avatar": avatar,
            "unread": unread_query.count(),
            "last_message": {
                "id": last_msg.id,
                "content": last_msg.content,
                "sender_id": last_msg.sender_id,
                "sender_username": last_msg.sender.username if last_msg.sender else None,
                "created_at": last_msg.created_at.isoformat(),
                "reply_to": ({
                    "id": last_msg.reply_to.id,
                    "content": last_msg.reply_to.content,
                    "sender_username": last_msg.reply_to.sender.username if last_msg.reply_to.sender else None
                } if last_msg.reply_to else None),
                "reactions": build_reactions(last_msg.id)
            }
        })

    results.sort(key=lambda c: c["last_message"]["created_at"], reverse=True)
    print("TOTAL INBOX ITEMS:", len(results), "\n================================\n")
    return results
