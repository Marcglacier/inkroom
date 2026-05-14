# app/notifications/services/create_comment_like.py
from .create_notification import (
    create_notification
)


def create_comment_like(actor_id, comment):

    if comment.user_id == actor_id:
        return None

    return create_notification(
        user_id=comment.user_id,
        actor_id=actor_id,
        type="LIKE_COMMENT",
        comment_id=comment.id,
        post_id=comment.post_id
    )