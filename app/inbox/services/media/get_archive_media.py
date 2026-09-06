# app/inbox/services/media/get_archive_media.py
from app.inbox.models.conversations.conversation_participant import ConversationParticipant
from app.inbox.models.messages.media_view import MediaView
from app.inbox.models.messages.message_media import MessageMedia
from app.storage.service import get_file_url

def get_archive_media(user_id: int, conversation_id: int):
    """
    Returns every piece of media the user has opened
    within a conversation.
    """

    participant = ConversationParticipant.query.filter_by(
        conversation_id=conversation_id,
        user_id=user_id,
    ).first()

    if participant is None:
        raise PermissionError(
            "You do not have access to this conversation."
        )

    views = (
        MediaView.query
        .join(MessageMedia, MediaView.media_id == MessageMedia.id)
        .filter(MediaView.user_id == user_id)
        .order_by(MessageMedia.created_at.desc())
        .all()
    )

    archive = []

    for view in views:

        media = MessageMedia.query.get(view.media_id)

        if media is None:
            continue

        message = media.message

        if message is None:
            continue

        if message.conversation_id != conversation_id:
            continue

        if message.deleted_for_everyone:
            continue

        if user_id in (message.deleted_for_users or []):
            continue

        archive.append({
            "id": media.id,
            "message_id": media.message_id,
            "sender_id": media.message.sender_id,
            "filename": media.filename,
            "mime_type": media.mime_type,
            "size": media.size,
            "url": get_file_url(media.object_key),
            "created_at": media.created_at.isoformat(),
            "opened_at": view.opened_at.isoformat(),
        })

    return archive