# app/inbox/services/links/permissions.py
from app.inbox.models.conversations.conversation_participant import (
    ConversationParticipant,
)
from app.inbox.models.messages.message_link import MessageLink


class LinkPermissionService:
    """
    Determines whether a user can access a message link.
    """

    def __init__(
        self,
        user_id: int,
        link: MessageLink,
    ):
        self.user_id = user_id
        self.link = link

    def can_access(self) -> bool:
        conversation_id = (
            self.link.message.conversation_id
        )

        participant = (
            ConversationParticipant.query
            .filter_by(
                conversation_id=conversation_id,
                user_id=self.user_id,
            )
            .first()
        )

        return participant is not None