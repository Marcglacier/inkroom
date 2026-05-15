# app/notifications/services/create_follow_accept_notification.py
from .create_notification import (
    create_notification
)


def create_follow_accept_notification(
    actor_id,
    target_user_id
):

    if actor_id == target_user_id:
        return None

    return create_notification(
        user_id=target_user_id,
        actor_id=actor_id,
        type="FOLLOW_ACCEPTED"
    )