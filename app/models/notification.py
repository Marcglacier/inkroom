# app/models/notification.py
from datetime import datetime
from app.extensions import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    
    # RECEIVER (who gets notif)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # ACTOR (who triggered it)
    actor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # CONTEXT OBJECTS
    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        nullable=True,
        index=True
    )

    comment_id = db.Column(
        db.Integer,
        db.ForeignKey("comments.id"),
        nullable=True,
        index=True
    )

    # TYPE
    type = db.Column(
        db.String(50),
        nullable=False,
        index=True
    )

    # STATUS
    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    # RELATIONSHIPS

    # receiver
    user = db.relationship(
        "User",
        foreign_keys=[user_id],
        backref=db.backref("notifications", lazy="dynamic")
    )

    # actor (trigger user)
    actor = db.relationship(
        "User",
        foreign_keys=[actor_id]
    )

    post = db.relationship(
        "Post",
        foreign_keys=[post_id]
    )

    comment = db.relationship(
        "Comment",
        foreign_keys=[comment_id]
    )

    # SERIALIZER
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat(),

            "actor": {
                "id": self.actor.id,
                "username": self.actor.username
            } if self.actor else None,

            "post": {
                "id": self.post.id,
                "title": self.post.title
            } if self.post else None,

            "comment": {
                "id": self.comment.id,
                "content": self.comment.content
            } if self.comment else None
        }