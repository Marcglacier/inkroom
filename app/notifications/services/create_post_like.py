# app/notifications/services/create_post_like.py
from .create_notification import create_notification
from .utils import should_notify


def create_post_like(actor_id, post):

    if not should_notify(actor_id, post.author_id):
        return None

    return create_notification(
        user_id=post.author_id,
        actor_id=actor_id,
        type="LIKE_POST",
        post_id=post.id
    )