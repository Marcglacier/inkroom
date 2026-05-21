# app/models/comment_like.py
from app.extensions import db


class CommentLike(db.Model):
    __tablename__ = "comment_likes"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    comment_id = db.Column(
        db.Integer,
        db.ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=False
    )