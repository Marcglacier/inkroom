# app/notifications/services/queries/get_unread_groups.py

from app.extensions import db
from app.models.notification import Notification
from app.notifications.constants import (
    LIKE_POST,
    COMMENT_POST,
    FOLLOW_USER,
    FOLLOW_REQUEST,
    FOLLOW_ACCEPT,
)


class GetUnreadGroupsService:

    NOTIFICATION_CATEGORIES = {
        "activity": {
            LIKE_POST,
            COMMENT_POST,
        },

        "follows": {
            FOLLOW_USER,
            FOLLOW_REQUEST,
            FOLLOW_ACCEPT,
        },

        # Mentions will be added when the Ink/post system is implemented.
        "mentions": set(),
    }

    def get(self, user_id: int) -> dict:

        rows = (
            db.session.query(
                Notification.type,
                db.func.count(Notification.id),
            )
            .filter(
                Notification.user_id == user_id,
                Notification.is_read.is_(False),
            )
            .group_by(Notification.type)
            .all()
        )

        unread_by_type = {
            notification_type: count
            for notification_type, count in rows
        }

        return {
            category: self._count_category(
                notification_types,
                unread_by_type,
            )
            for category, notification_types
            in self.NOTIFICATION_CATEGORIES.items()
        }

    def _count_category(
        self,
        notification_types: set[str],
        unread_by_type: dict,
    ) -> int:

        return sum(
            unread_by_type.get(notification_type, 0)
            for notification_type in notification_types
        )


get_unread_groups_service = GetUnreadGroupsService()