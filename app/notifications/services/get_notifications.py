# app/notifications/services/get_notifications.py
from app.models.notification import Notification


def get_notifications(user_id):

    notifications = Notification.query.filter_by(
        user_id=user_id
    ).order_by(
        Notification.created_at.desc()
    ).all()

    return [
        notification.to_dict()
        for notification in notifications
    ]