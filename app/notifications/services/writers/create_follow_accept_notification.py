# app/notifications/services/create_follow_accept_notification.py
from .create_notification import (
    notification_creator
)


def create_follow_accept_notification(
    actor_id,
    target_user_id
):

    if actor_id == target_user_id:
        return None

    return notification_creator(
        user_id=target_user_id,
        actor_id=actor_id,
        type="FOLLOW_ACCEPTED"
    )