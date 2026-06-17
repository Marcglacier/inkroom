# app/models/comment.py

from datetime import datetime
from app.extensions import db


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    parent_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship(
        "User",
        backref=db.backref("comments", lazy=True),
        lazy=True
    )

    post = db.relationship(
    "Post",
    back_populates="comments",
    lazy=True
    )

    parent = db.relationship(
        "Comment",
        remote_side=[id],
        backref=db.backref("replies", lazy=True)
    )

    likes = db.relationship(
        "CommentLike",
        backref="comment",
        cascade="all, delete-orphan",
        lazy=True
    )