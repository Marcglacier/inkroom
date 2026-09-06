# app/inbox/services/messages/fetch_pinned_messages.py
from app.storage.service import get_file_url
from app.inbox.models.messages.pinned_message import PinnedMessage
from app.inbox.models.messages.message import Message
from app.models.user import User
from app.inbox.services.conversations.core.conversation_guard import ( ConversationGuard, )
from app.inbox.models.conversations.conversation_clear import ConversationClear

def fetch_pinned(conversation_id, user_id):

    ConversationGuard.require_participant( conversation_id, user_id, )

    pins = PinnedMessage.query.filter_by(
        conversation_id=conversation_id
    ).all()
    clear = ConversationClear.query.filter_by(
        conversation_id=conversation_id,
        user_id=user_id
    ).first()

    results = []

    for p in pins:

        msg = Message.query.get(p.message_id)

        if not msg:
            continue

        # Hidden by conversation clear
        if ( clear and msg.created_at <= clear.cleared_at ):
         continue

        # Message deleted for everyone
        if msg.deleted_for_everyone:
            continue

        # Message deleted only for this user
        if user_id in (msg.deleted_for_users or []):
            continue

        sender = User.query.get(msg.sender_id)
        pinner = User.query.get(p.pinned_by)

        results.append({
            "message_id": msg.id,
            "content": msg.content,
            "sender": {
                "id": sender.id,
                "name": sender.name,
                "username": sender.username,
                "avatar": ( get_file_url(sender.profile_picture)
                    if sender and sender.profile_picture else None
                ),                
            } if sender else None,
            "pinned_by": {
                "id": pinner.id,
                "name": pinner.name,
                "username": pinner.username
            } if pinner else None,
            "pinned_at": p.pinned_at
        })

    return results