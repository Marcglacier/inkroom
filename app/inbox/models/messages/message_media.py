# app/inbox/models/message_media.py

from datetime import datetime

from app.extensions import db


class MessageMedia(db.Model):
    __tablename__ = "message_media"

    id = db.Column(db.Integer, primary_key=True)

    message_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    object_key = db.Column(
        db.Text,
        nullable=False,
    )

    filename = db.Column(
        db.String(255),
        nullable=False,
    )

    mime_type = db.Column(
        db.String(120),
        nullable=False,
    )

    size = db.Column(
        db.BigInteger,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    #-----------General media metadata----------

    media_kind = db.Column(
        db.String(20),
        nullable=False,
        default="file",
    )

    # Future (optional)
    waveform = db.Column(
        db.JSON,
        nullable=True,
    )

    # ---------- Audio metadata ----------
    title = db.Column( db.String(255), nullable=True, )

    artist = db.Column( db.String(255), nullable=True, )

    album = db.Column( db.String(255), nullable=True, )

    duration = db.Column( db.Integer, nullable=True, )

    cover_object_key = db.Column( db.Text, nullable=True, )

    # ---------- Video metadata ----------

    video_width = db.Column( db.Integer, nullable=True, )

    video_height = db.Column( db.Integer, nullable=True, )
    
    thumbnail_object_key = db.Column( db.Text, nullable=True, )

    # ------------------------------------

    message = db.relationship(
        "Message",
        back_populates="media",
    )

    views = db.relationship(
        "MediaView",
        backref="media",
        cascade="all, delete-orphan",
        lazy=True,
    )

