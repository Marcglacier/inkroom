# app/notifications/services/create_post_repost.py
from .create_notification import create_notification
from .utils import should_notify

def create_post_repost(actor_id, post):

    if actor_id == post.author_id:
        return

    create_notification(
        actor_id=actor_id,
        user_id=post.author_id,
        type="REPOST",
        post_id=post.id
    )