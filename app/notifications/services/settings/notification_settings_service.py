# app/notifications/services/settings/notification_settings_service.py
from datetime import datetime, timedelta

from app.extensions import db
from app.models.notification_settings import NotificationSettings


class NotificationSettingsService:

    ALLOWED_DURATIONS = {
        "15m": timedelta(minutes=15),
        "1h": timedelta(hours=1),
        "4h": timedelta(hours=4),
        "8h": timedelta(hours=8),
        "24h": timedelta(hours=24),
    }

    @staticmethod
    def _serialize_datetime(value):
        if not value:
            return None

        return f"{value.isoformat()}Z"
        
    def _get_or_create(self, user_id: int):
        settings = NotificationSettings.query.filter_by(
            user_id=user_id
        ).first()

        if not settings:
            settings = NotificationSettings(
                user_id=user_id
            )

            db.session.add(settings)
            db.session.commit()

        return settings

    def get(self, user_id: int) -> dict:
        settings = self._get_or_create(user_id)

        muted = settings.is_muted

        # Automatically treat expired mute as inactive.
        if settings.muted_until and not muted:
            settings.muted_until = None
            db.session.commit()

        return {
            "muted": muted,
            "muted_until": (
                self._serialize_datetime(settings.muted_until)
                if muted
                else None
            ),
        }

    def mute(
        self,
        user_id: int,
        duration: str,
    ) -> dict:

        if duration not in self.ALLOWED_DURATIONS:
            raise ValueError(
                "Invalid notification mute duration"
            )

        settings = self._get_or_create(user_id)

        settings.muted_until = (
            datetime.utcnow()
            + self.ALLOWED_DURATIONS[duration]
        )

        db.session.commit()

        return {
            "muted": True,
            "muted_until": self._serialize_datetime(
                settings.muted_until
            ),
        }

    def unmute(self, user_id: int) -> dict:
        settings = self._get_or_create(user_id)

        settings.muted_until = None

        db.session.commit()

        return {
            "muted": False,
            "muted_until": None,
        }


notification_settings_service = (
    NotificationSettingsService()
)