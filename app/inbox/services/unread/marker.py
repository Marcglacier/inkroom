# marker.py

from app.inbox.models import ConversationParticipant


def get_session_unread_marker(
    participant: ConversationParticipant | None,
):
    if not participant:
        return None

    return participant.last_read_message_id