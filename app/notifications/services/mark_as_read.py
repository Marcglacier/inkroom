# app/notifications/services/mark_as_read.py
from app.extensions import db
from app.models.notification import Notification


def mark_as_read(notification_id, user_id):

    notification = Notification.query.filter_by(
        id=notification_id,
        user_id=user_id
    ).first()

    if not notification:
        return {
            "error": "Notification not found"
        }, 404

    notification.is_read = True

    db.session.commit()

    return {
        "message": "Notification marked as read"
    }, 200