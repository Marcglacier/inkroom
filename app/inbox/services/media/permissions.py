# app/inbox/services/media/permissions.py

from app.inbox.models.conversations.conversation_participant import ConversationParticipant
from app.inbox.models.messages.message_media import MessageMedia


def can_access_media(user_id: int, media: MessageMedia) -> bool:
    """
    Returns True if the user belongs to the conversation
    containing this media.
    """

    conversation_id = media.message.conversation_id

    participant = ConversationParticipant.query.filter_by(
        conversation_id=conversation_id,
        user_id=user_id,
    ).first()

    return participant is not None