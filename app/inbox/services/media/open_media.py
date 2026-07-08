# app/inbox/services/media/open_media.py

from app.inbox.models.message_media import MessageMedia
from app.inbox.services.media.permissions import can_access_media
from app.inbox.services.media.media_view import record_media_view


def open_media(user_id: int, media_id: int):
    """
    Records that a user opened a piece of media.
    """

    media = MessageMedia.query.get(media_id)

    if media is None:
        raise ValueError("Media not found")

    if not can_access_media(user_id, media):
        raise PermissionError(
            "You do not have access to this media."
        )

    record_media_view(
        user_id=user_id,
        media_id=media.id,
    )

    return {
        "success": True,
        "media_id": media.id,
    }