# app/notifications/services/create_comment_like.py
from .create_notification import create_notification
from .utils import should_notify
from app.notifications.constants import COMMENT_POST

def create_comment_like(actor_id, comment):

    if not should_notify(actor_id, comment.user_id):
        return None

    return create_notification(
        user_id=comment.user_id,
        actor_id=actor_id,
        type=COMMENT_POST,
        comment_id=comment.id,
        post_id=comment.post_id
    )