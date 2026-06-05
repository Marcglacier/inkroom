# app/notifications/services/readers/get_notifications.py

from app.models.notification import Notification


def get_notifications(user_id):

    notifications = (
        Notification.query
        .filter_by(user_id=user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    result = []

    for n in notifications:

        result.append({
            "id": n.id,
            "type": n.type,
            "is_read": n.is_read,
            "created_at": n.created_at,

            "actor": {
                "id": n.actor.id if n.actor else None,
                "username": n.actor.username if n.actor else None,
                "avatar": getattr(n.actor, "profile_picture", None),
            } if hasattr(n, "actor") else None,

            "extra": {
                "post_id": getattr(n, "post_id", None),
                "comment_id": getattr(n, "comment_id", None),
            }
        })

    return result