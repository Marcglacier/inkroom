# app/inbox/services/links/link_view.py
from datetime import datetime

from app.extensions import db
from app.inbox.models.messages.link_view import LinkView


class LinkViewService:
    """
    Creates or updates a user's view of a message link.
    """

    def __init__(
        self,
        user_id: int,
        link_id: int,
    ):
        self.user_id = user_id
        self.link_id = link_id

    def execute(self) -> LinkView:
        view = (
            LinkView.query
            .filter_by(
                link_id=self.link_id,
                user_id=self.user_id,
            )
            .first()
        )

        if view:
            view.opened_at = datetime.utcnow()

        else:
            view = LinkView(
                link_id=self.link_id,
                user_id=self.user_id,
            )

            db.session.add(view)

        db.session.commit()

        return view