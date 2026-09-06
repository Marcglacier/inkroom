# app/notifications/services/create_post_like.py
from .create_notification import notification_creator
from app.notifications.constants import LIKE_POST

def create_post_like(actor_id, post):

    if actor_id == post.author_id:
        return

    notification_creator(
        actor_id=actor_id,
        user_id=post.author_id,
        type=LIKE_POST,
        post_id=post.id
    )