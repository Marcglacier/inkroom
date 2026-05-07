# app/inbox/services/inbox/get_other_user.py

from app.inbox.models.conversation_participant import ConversationParticipant
from app.models.user import User


def get_other_user(conversation_id, current_user):

    other = ConversationParticipant.query.filter(
        ConversationParticipant.conversation_id == conversation_id,
        ConversationParticipant.user_id != current_user
    ).first()

    if not other:
        return None

    return User.query.get(other.user_id)