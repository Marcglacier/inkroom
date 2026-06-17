from app.extensions import db
from app.models.notification import Notification


def get_unread_groups(user_id):
    rows = (
        db.session.query(
            Notification.type,
            db.func.count(Notification.id)
        )
        .filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        )
        .group_by(Notification.type)
        .all()
    )

    return {
        notification_type: count
        for notification_type, count in rows
    }