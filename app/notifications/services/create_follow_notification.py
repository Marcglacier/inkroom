# app/notifications/services/create_follow_notification.py
from .create_notification import create_notification
from .utils import should_notify


def create_follow_notification(actor_id, target_user_id):

    if not should_notify(actor_id, target_user_id):
        return None

    return create_notification(
        user_id=target_user_id,
        actor_id=actor_id,
        type="FOLLOW_USER"
    )