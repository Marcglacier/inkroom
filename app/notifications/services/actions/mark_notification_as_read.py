# app/notifications/services/actions/mark_notification_as_read.py

from app.extensions import db
from app.models.notification import Notification
from app.notifications.constants import (
    LIKE_POST,
    COMMENT_POST,
    FOLLOW_USER,
    FOLLOW_REQUEST,
    FOLLOW_ACCEPT,
)


class MarkNotificationAsReadService:

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
    }

    def mark(self, user_id: int, notification_type: str) -> dict:
        notification_types = self._resolve_types(
            notification_type
        )

        updated = (
            Notification.query
            .filter(
                Notification.user_id == user_id,
                Notification.type.in_(notification_types),
                Notification.is_read.is_(False),
            )
            .update(
                {
                    "is_read": True
                },
                synchronize_session=False,
            )
        )

        db.session.commit()

        return {
            "message": (
                f"{notification_type} notifications "
                "marked as read"
            ),
            "updated_count": updated,
        }

    def _resolve_types(
        self,
        notification_type: str,
    ) -> set[str]:

        category_types = self.NOTIFICATION_CATEGORIES.get(
            notification_type
        )

        if category_types:
            return category_types

        return {notification_type}


mark_notification_as_read_service = (
    MarkNotificationAsReadService()
)