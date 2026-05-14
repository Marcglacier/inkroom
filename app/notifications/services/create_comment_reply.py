# app/notifications/services/create_comment_reply.py
from .create_notification import (
    create_notification
)

def create_comment_reply(
    actor_id,
    parent_comment,
    reply_comment
):

    if parent_comment.user_id == actor_id:
        return None

    return create_notification(
        user_id=parent_comment.user_id,
        actor_id=actor_id,
        type="REPLY_COMMENT",
        post_id=reply_comment.post_id,
        comment_id=reply_comment.id
    )