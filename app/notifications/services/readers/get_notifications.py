# app/notifications/services/readers/get_notifications.py

from app.models.notification import Notification
from app.notifications.services.core.group_notifications import group_notifications
from app.notifications.services.core.notification_messages import build_notification_message
import inspect

# 🔥 DEBUG: confirm which function is loaded
print("🔥 USING:", inspect.getsource(build_notification_message))


def get_notifications(user_id):

    notifications = (
        Notification.query
        .filter_by(user_id=user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    grouped = group_notifications(notifications)

    result = []

    for group in grouped:

        # 🧠 DEBUG: ensure structure is correct


        # 🔥 SAFETY CHECK (prevents future silent crashes)
        if "type" not in group or "actors" not in group:
            print("❌ INVALID GROUP FORMAT:", group)
            continue

        message = build_notification_message(group)

        result.append({
            "type": group["type"],
            "message": message,
            "count": len(group["raw_notifications"]),
            "post_id": group["post_id"],
            "comment_id": group["comment_id"],
            "actors": group["actors"],
            "latest_created_at": group["latest_created_at"]
        })

    return result