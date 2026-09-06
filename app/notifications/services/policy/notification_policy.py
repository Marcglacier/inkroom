# app/notifications/services/policy/notification_policy.py
from app.models.notification_settings import (
    NotificationSettings,
)


class NotificationPolicy:

    @staticmethod
    def is_muted(user_id: int) -> bool:

        settings = NotificationSettings.query.filter_by(
            user_id=user_id
        ).first()

        if not settings:
            return False

        return settings.is_muted

    @staticmethod
    def state(user_id: int) -> dict:

        settings = NotificationSettings.query.filter_by(
            user_id=user_id
        ).first()

        if not settings:
            return {
                "muted": False,
                "muted_until": None,
            }

        if not settings.is_muted:
            return {
                "muted": False,
                "muted_until": None,
            }

        return {
            "muted": True,
            "muted_until": settings.muted_until.isoformat(),
        }


notification_policy = NotificationPolicy()