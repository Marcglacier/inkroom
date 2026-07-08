from app.inbox.models import (
    ConversationParticipant,
    ConversationClear,
    ConversationRequest,
    Message,
)
from app.models.user import User
from app.inbox.services.messages.message_reaction_aggregator import (
    build_reactions,
)
from app.storage.service import get_file_url

def build_conversation_card(convo, user_id):
    print("🔥🔥🔥 GET_INBOX CALLED 🔥🔥🔥")
    """
    Builds the inbox card for one conversation.
    Returns None if the conversation should not appear.
    """

    # -----------------------------
    # Hide pending/rejected requests
    # -----------------------------
    if convo.status == "pending":
        req = ConversationRequest.query.filter_by(
            conversation_id=convo.id
        ).first()

        if req and req.receiver_id == user_id:
            return None

    if convo.status == "rejected":
        req = ConversationRequest.query.filter_by(
            conversation_id=convo.id
        ).first()

        if req and req.receiver_id == user_id:
            return None

    # -----------------------------
    # Participants
    # -----------------------------
    participants = ConversationParticipant.query.filter_by(
        conversation_id=convo.id
    ).all()

    if not participants:
        return None

    # Saved Messages
    if len(participants) == 1 and participants[0].user_id == user_id:
        other_user_id = user_id
        username = "Saved Messages"
        name = "Saved Messages"
        avatar = None
    else:
        other = next(
            (p for p in participants if p.user_id != user_id),
            None,
        )

        if not other:
            return None

        user = User.query.get(other.user_id)

        if not user:
            return None

        other_user_id = user.id
        username = user.username
        name = user.name
        avatar = (get_file_url(user.profile_picture)
                  if user.profile_picture else None)

        print(f"\nConversation {convo.id}")

    for p in participants:
      print(
         "participant:",
          p.user_id
        )

    # -----------------------------
    # Cleared conversations
    # -----------------------------
    clear = ConversationClear.query.filter_by(
        conversation_id=convo.id,
        user_id=user_id,
    ).first()

    msg_query = Message.query.filter(
        Message.conversation_id == convo.id,
        Message.deleted_for_everyone.is_(False),
    )

    if clear:
        msg_query = msg_query.filter(
            Message.created_at > clear.cleared_at
        )

    last_msg = (
        msg_query.order_by(
            Message.created_at.desc()
        ).first()
    )

    if not last_msg:
        return None

    unread_query = Message.query.filter(
        Message.conversation_id == convo.id,
        Message.sender_id != user_id,
        Message.read_at.is_(None),
        Message.deleted_for_everyone.is_(False),
    )

    if clear:
        unread_query = unread_query.filter(
            Message.created_at > clear.cleared_at
        )

    return {
        "conversation_id": convo.id,
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
    "sender_username": (
        last_msg.sender.username
        if last_msg.sender
        else None
    ),
    "created_at": last_msg.created_at.isoformat(),

    # NEW
    "status": last_msg.status,
    "delivered_at": (
        last_msg.delivered_at.isoformat()
        if last_msg.delivered_at
        else None
    ),
    "read_at": (
        last_msg.read_at.isoformat()
        if last_msg.read_at
        else None
    ),
    "edited": last_msg.edited,
    "deleted_for_everyone": last_msg.deleted_for_everyone,
    "is_mine": last_msg.sender_id == user_id,

    "reply_to": (
        {
            "id": last_msg.reply_to.id,
            "content": last_msg.reply_to.content,
            "sender_username": (
                last_msg.reply_to.sender.username
                if last_msg.reply_to.sender
                else None
            ),
        }
        if last_msg.reply_to
        else None
    ),

    "reactions": build_reactions(last_msg.id),
    
    },
    
    }