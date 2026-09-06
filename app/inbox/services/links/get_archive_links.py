# app/inbox/services/links/get_archive_links.py
from app.inbox.models.conversations.conversation_participant import (
    ConversationParticipant,
)
from app.inbox.models.messages.link_view import LinkView
from app.inbox.models.messages.message_link import MessageLink


class GetArchiveLinksService:
    """
    Returns every link the user has opened
    within a conversation.
    """

    def __init__(
        self,
        user_id: int,
        conversation_id: int,
    ):
        self.user_id = user_id
        self.conversation_id = conversation_id

    def execute(self) -> list[dict]:
        self._verify_participant()

        views = (
            LinkView.query
            .join(
                MessageLink,
                LinkView.link_id == MessageLink.id,
            )
            .filter(
                LinkView.user_id == self.user_id,
            )
            .order_by(
                MessageLink.created_at.desc()
            )
            .all()
        )

        archive = []

        for view in views:
            link = view.link

            if link is None:
                continue

            if (
                link.message.conversation_id
                != self.conversation_id
            ):
                continue

            archive.append({
                **link.to_dict(),
                "opened_at": (
                    view.opened_at.isoformat() + "Z"
                    if view.opened_at
                    else None
                ),
            })

        return archive

    def _verify_participant(self) -> None:
        participant = (
            ConversationParticipant.query
            .filter_by(
                conversation_id=self.conversation_id,
                user_id=self.user_id,
            )
            .first()
        )

        if participant is None:
            raise PermissionError(
                "You do not have access to this conversation."
            )