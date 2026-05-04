# app/models/post_like.py
from app.extensions import db


class PostLike(db.Model):
    __tablename__ = "post_likes"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id", ondelete="CASCADE"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "post_id",
            name="unique_user_post_like"
        ),
        db.Index("idx_post_like_post_id", "post_id"),
        db.Index("idx_post_like_user_id", "user_id"),
    )