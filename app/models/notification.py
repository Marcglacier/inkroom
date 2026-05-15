from datetime import datetime

from app.extensions import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    actor_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        nullable=True
    )

    comment_id = db.Column(
        db.Integer,
        db.ForeignKey("comments.id"),
        nullable=True
    )

    type = db.Column(
        db.String(50),
        nullable=False
    )

    is_read = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # =========================
    # RELATIONSHIPS
    # =========================

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

    # =========================
    # SERIALIZER
    # =========================

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