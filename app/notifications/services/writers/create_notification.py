# app/notifications/services/writers/create_notification.py

from app.extensions import db, socketio
from app.models.notification import Notification

from app.notifications.services.socket_events import emit_notification

# notification types that should NOT duplicate
DEDUPE_TYPES = {
    "LIKE_POST",
    "LIKE_COMMENT",
    "FOLLOW_USER",
    "FOLLOW_REQUEST"
}


def create_notification(**kwargs):

    notif_type = kwargs.get("type")

    print("\n🔥 [NOTIF DEBUG] create_notification CALLED")
    print("➡️ type:", notif_type)
    print("➡️ user_id (receiver):", kwargs.get("user_id"))
    print("➡️ actor_id:", kwargs.get("actor_id"))
    print("➡️ post_id:", kwargs.get("post_id"))
    print("➡️ comment_id:", kwargs.get("comment_id"))

    # =====================================
    # GROUP / DEDUPE CHECK
    # =====================================
    if notif_type in DEDUPE_TYPES:

        print("⚠️ Dedup enabled for:", notif_type)

        existing = Notification.query.filter_by(
            user_id=kwargs.get("user_id"),
            type=notif_type,
            post_id=kwargs.get("post_id"),
            comment_id=kwargs.get("comment_id"),
            is_read=False
        ).first()

        # =====================================
        # UPDATE EXISTING GROUP
        # =====================================
        if existing:

            print("⚠️ EXISTING GROUP FOUND:", existing.id)

            actors = []

            if isinstance(existing.extra, dict):
                actors = existing.extra.get("actors", [])

            new_actor = kwargs.get("actor_id")

            if new_actor not in actors:
                actors.append(new_actor)

            existing.extra = existing.extra or {}
            existing.extra["actors"] = actors

            db.session.commit()

            print("✅ Updated grouped notification:", existing.id)

            # 🔥 REAL-TIME EMIT (GROUP UPDATE)
            emit_notification(kwargs.get("user_id"), {
                "type": notif_type,
                "notification_id": existing.id,
                "message": "Notification updated",
                "actors": actors,
                "is_update": True
            })

            return existing

    # =====================================
    # CREATE NEW NOTIFICATION
    # =====================================
    print("🟢 Creating new notification...")

    notif = Notification(**kwargs)

    notif.extra = {
        "actors": [kwargs.get("actor_id")]
    }

    db.session.add(notif)
    db.session.commit()

    print("✅ Saved notification ID:", notif.id)

    # 🔥 REAL-TIME EMIT (NEW NOTIFICATION)
    emit_notification(kwargs.get("user_id"), {
        "type": notif.type,
        "notification_id": notif.id,
        "message": "New notification",
        "actors": notif.extra["actors"],
        "is_update": False
    })

    return notif