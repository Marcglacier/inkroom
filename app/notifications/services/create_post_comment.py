# app/notifications/services/create_post_comment.py
from .create_notification import (
    create_notification
)


def create_post_comment(actor_id, post, comment):

    if post.author_id == actor_id:
        return None

    return create_notification(
        user_id=post.author_id,
        actor_id=actor_id,
        type="COMMENT_POST",
        post_id=post.id,
        comment_id=comment.id
    )