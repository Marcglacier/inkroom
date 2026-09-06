# app/notifications/services/create_follow_request_notification.py
from .create_notification import notification_creator
from .utils import should_notify
from app.notifications.constants import FOLLOW_REQUEST


def create_follow_request_notification(actor_id, target_user_id):

    if not should_notify(actor_id, target_user_id):
        return None

    return notification_creator(
        user_id=target_user_id,
        actor_id=actor_id,
        type=FOLLOW_REQUEST
    )