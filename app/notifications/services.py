# app/notifications/services.py

from app.extensions import db
from app.models.notification import Notification


class NotificationService:

    @staticmethod
    def create_post_like(actor_id, post):
        if post.author_id == actor_id:
            return None

        notif = Notification(
            user_id=post.author_id,
            actor_id=actor_id,
            type="LIKE_POST",
            post_id=post.id
        )

        db.session.add(notif)
        db.session.commit()
        return notif

    @staticmethod
    def create_post_comment(actor_id, post, comment):
        if post.author_id == actor_id:
            return None

        notif = Notification(
            user_id=post.author_id,
            actor_id=actor_id,
            type="COMMENT_POST",
            post_id=post.id,
            comment_id=comment.id
        )

        db.session.add(notif)
        db.session.commit()
        return notif

    @staticmethod
    def create_comment_like(actor_id, comment):
        if comment.user_id == actor_id:
            return None

        notif = Notification(
            user_id=comment.user_id,
            actor_id=actor_id,
            type="LIKE_COMMENT",
            comment_id=comment.id,
            post_id=comment.post_id
        )

        db.session.add(notif)
        db.session.commit()
        return notif

    @staticmethod
    def create_comment_reply(actor_id, parent_comment, reply_comment):
        if parent_comment.user_id == actor_id:
            return None

        notif = Notification(
            user_id=parent_comment.user_id,
            actor_id=actor_id,
            type="REPLY_COMMENT",
            post_id=reply_comment.post_id,
            comment_id=reply_comment.id
        )

        db.session.add(notif)
        db.session.commit()
        return notif