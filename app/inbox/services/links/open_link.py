# app/inbox/services/links/open_link.py
from app.inbox.models.messages.message_link import MessageLink
from app.inbox.services.links.permissions import (
    LinkPermissionService,
)
from app.inbox.services.links.link_view import (
    LinkViewService,
)


class OpenLinkService:
    """
    Handles opening a message link.

    Responsibilities:
    - retrieve the link
    - verify access
    - record the user's interaction
    """

    def __init__(
        self,
        user_id: int,
        link_id: int,
    ):
        self.user_id = user_id
        self.link_id = link_id

    def execute(self) -> dict:
        link = self._get_link()

        self._verify_access(link)

        LinkViewService(
            user_id=self.user_id,
            link_id=link.id,
        ).execute()

        return {
            "success": True,
            "link_id": link.id,
        }

    def _get_link(self) -> MessageLink:
        link = MessageLink.query.get(self.link_id)

        if link is None:
            raise ValueError("Link not found")

        return link

    def _verify_access(
        self,
        link: MessageLink,
    ) -> None:

        allowed = LinkPermissionService(
            user_id=self.user_id,
            link=link,
        ).can_access()

        if not allowed:
            raise PermissionError(
                "You do not have access to this link."
            )