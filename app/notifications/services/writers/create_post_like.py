# app/notifications/services/create_post_like.py
from .create_notification import create_notification
from .utils import should_notify
from app.notifications.constants import LIKE_POST

def create_post_like(actor_id, post):

    if actor_id == post.author_id:
        return

    create_notification(
        actor_id=actor_id,
        user_id=post.author_id,
        type=LIKE_POST,
        post_id=post.id
    )