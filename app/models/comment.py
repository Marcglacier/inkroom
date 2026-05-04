# app/models/comment.py

from datetime import datetime
from app.extensions import db


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)

    content = db.Column(
        db.Text,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        nullable=False
    )

    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("comments.id"),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # =========================
    # REPLIES (THREADING)
    # =========================

    parent = db.relationship(
        "Comment",
        remote_side=[id],
        backref=db.backref(
            "replies",
            cascade="all, delete-orphan",
            lazy=True
        )
    )

    # =========================
    # COMMENT LIKES
    # =========================

    likes = db.relationship(
        "CommentLike",
        backref="comment",
        cascade="all, delete-orphan",
        lazy=True
    )