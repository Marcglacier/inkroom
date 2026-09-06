# app/notifications/services/writers/create_notification.py

from app.extensions import db
from app.models.notification import Notification
from app.models.user import User
from app.storage.service import get_file_url
from app.notifications.services.socket_events import emit_notification
from app.notifications.services.policy.notification_policy import (
    notification_policy,
)

class NotificationCreator:

    DEDUPE_TYPES = {
        "LIKE_POST",
        "LIKE_COMMENT",
        "FOLLOW_USER",
        "FOLLOW_REQUEST",
    }

    def create(self, **kwargs):

        notif_type = kwargs.get("type")
        receiver_id = kwargs.get("user_id")
        actor_id = kwargs.get("actor_id")

        print("\n🔥 [NOTIF DEBUG] NotificationCreator.create()")
        print("➡️ type:", notif_type)
        print("➡️ receiver:", receiver_id)
        print("➡️ actor:", actor_id)   

        actor = User.query.get(actor_id)

        if not actor:
            print("⚠️ Actor not found:", actor_id)
            return None

        # GROUP / DEDUPE
        if notif_type in self.DEDUPE_TYPES:

            existing = Notification.query.filter_by(
                user_id=receiver_id,
                type=notif_type,
                post_id=kwargs.get("post_id"),
                comment_id=kwargs.get("comment_id"),
                is_read=False,
            ).first()

            if existing:
                return self._update_existing(
                    existing,
                    actor,
                )

        # CREATE
        return self._create_new(
            kwargs,
            actor,
        )

    # UPDATE EXISTING GROUP
    def _update_existing(self, notification, actor):

        print(
            "⚠️ EXISTING GROUP FOUND:",
            notification.id,
        )

        actors = []

        if isinstance(notification.extra, dict):
            actors = notification.extra.get(
                "actors",
                [],
            )

        # Don't duplicate actor
        if not any(
            existing_actor.get("id") == actor.id
            for existing_actor in actors
            if isinstance(existing_actor, dict)
        ):
            actors.append(
                self._actor_data(actor)
            )

        notification.extra = {
            **(notification.extra or {}),
            "actors": actors,
        }

        db.session.commit()

        print(
            "✅ Updated grouped notification:",
            notification.id,
        )

        if notification_policy.is_muted(notification.user_id):
            print( "🔕 Notifications muted for user:", notification.user_id, )
        else:
            self._emit(
                notification,
                actors,
                is_update=True,
            )

        return notification

    # CREATE NEW
    def _create_new(self, kwargs, actor):

        print("🟢 Creating new notification...")

        notification = Notification(**kwargs)

        notification.extra = {
            "actors": [
                self._actor_data(actor)
            ]
        }

        db.session.add(notification)
        db.session.commit()

        print(
            "✅ Saved notification ID:",
            notification.id,
        )

        if notification_policy.is_muted(notification.user_id):
            print( "🔕 Notifications muted for user:", notification.user_id, )
        else:
            self._emit(
                notification,
                notification.extra["actors"],
                is_update=False,
            )

        return notification

    # ACTOR DATA
    @staticmethod
    def _actor_data(actor):

        return {
            "id": actor.id,
            "username": actor.username,
            "name": actor.name,
            "avatar": ( get_file_url(actor.profile_picture) if actor.profile_picture else None),
        }
    
    # SOCKET
    @staticmethod
    def _emit(notification, actors, is_update):

        emit_notification(
            notification.user_id,
            {
                "type": notification.type,
                "notification_id": notification.id,
                "message": (
                    "Notification updated"
                    if is_update
                    else "New notification"
                ),
                "actors": actors,
                "is_update": is_update,
            },
        )

notification_creator = NotificationCreator()

def create_notification(**kwargs):
    return notification_creator.create(**kwargs)