# app/notifications/services/create_notification.py

from app.extensions import db
from app.models.notification import Notification


# notification types that should NOT duplicate
DEDUPE_TYPES = {
    "LIKE_POST",
    "LIKE_COMMENT",
    "FOLLOW_USER",
    "FOLLOW_REQUEST"
}


def create_notification(**kwargs):

    notif_type = kwargs.get("type")

    # =====================================
    # DUPLICATE PREVENTION
    # =====================================
    if notif_type in DEDUPE_TYPES:

        existing = Notification.query.filter_by(
            user_id=kwargs.get("user_id"),
            actor_id=kwargs.get("actor_id"),
            type=notif_type,
            post_id=kwargs.get("post_id"),
            comment_id=kwargs.get("comment_id"),
            is_read=False
        ).first()

        if existing:
            return existing

    # =====================================
    # CREATE NEW NOTIFICATION
    # =====================================
    notif = Notification(**kwargs)

    db.session.add(notif)
    db.session.commit()

    return notif