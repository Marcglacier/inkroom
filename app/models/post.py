from datetime import datetime
from app.extensions import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False,
        index=True
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    author_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Cached like counter (important for performance)
    likes_count = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # Relationships
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