# app/notifications/services/create_comment_reply.py
from .create_notification import notification_creator
from .utils import should_notify
from app.notifications.constants import COMMENT_POST

def create_comment_reply(actor_id, parent_comment, reply_comment):

    if not should_notify(actor_id, parent_comment.user_id):
        return None

    return notification_creator(
        user_id=parent_comment.user_id,
        actor_id=actor_id,
        type=COMMENT_POST,
        post_id=reply_comment.post_id,
        comment_id=reply_comment.id
    )