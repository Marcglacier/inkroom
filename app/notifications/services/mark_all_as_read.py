# app/notifications/services/mark_all_as_read.py
from app.extensions import db
from app.models.notification import Notification


def mark_all_as_read(user_id):

    Notification.query.filter_by(
        user_id=user_id,
        is_read=False
    ).update({
        "is_read": True
    })

    db.session.commit()

    return {
        "message": "All notifications marked as read"
    }