# app/notifications/services/create_post_repost.py
from .create_notification import notification_creator
from app.notifications.constants import REPOST_POST


def create_post_repost(actor_id, post):

    if actor_id == post.author_id:
        return

    notification_creator(
        actor_id=actor_id,
        user_id=post.author_id,
        type=REPOST_POST,
        post_id=post.id
    )