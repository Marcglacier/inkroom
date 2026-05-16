# app/models/post.py
from datetime import datetime
from app.extensions import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)

    author_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # =========================
    # COUNTERS (FOR PERFORMANCE)
    # =========================
    likes_count = db.Column(db.Integer, default=0, nullable=False)
    comments_count = db.Column(db.Integer, default=0, nullable=False)
    reposts_count = db.Column(db.Integer, default=0, nullable=False)

    # =========================
    # TIMESTAMPS
    # =========================
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # =========================
    # RELATIONSHIPS
    # =========================

    author = db.relationship(
        "User",
        backref=db.backref("posts", lazy=True),
        lazy=True
    )

    comments = db.relationship(
        "Comment",
        backref="post",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    likes = db.relationship(
        "Like",
        backref="post",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    # (OPTIONAL FUTURE FEATURE)
    reposts = db.relationship(
        "Repost",
        backref="post",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )