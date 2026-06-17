# app/notifications/services/actions/mark_type_as_read.py
from app.extensions import db
from app.models.notification import Notification


def mark_type_as_read(user_id, notification_type):

    updated = Notification.query.filter_by(
        user_id=user_id,
        type=notification_type,
        is_read=False
    ).update({
        "is_read": True
    })

    db.session.commit()

    return {
        "message": f"{notification_type} notifications marked as read",
        "updated_count": updated
    }