# app/notifications/services/create_post_comment.py
from .create_notification import notification_creator


def create_post_comment(actor_id, post, comment):

    if actor_id == post.author_id:
        return  # 🚫 don't notify yourself

    notification_creator(
        actor_id=actor_id,
        user_id=post.author_id,   # 🔥 THIS IS THE KEY FIX
        type="COMMENT",
        post_id=post.id,
        comment_id=comment.id
    )