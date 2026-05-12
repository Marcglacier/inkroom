# app/inbox/models/message_media.py
from app.extensions import db


class MessageMedia(db.Model):
    __tablename__ = "message_media"

    id = db.Column(db.Integer, primary_key=True)

    message_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id", ondelete="CASCADE"),
        nullable=False
    )

    file_url = db.Column(db.Text, nullable=False)

    file_type = db.Column(db.String(20))  # image/video/file

    uploaded_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    message = db.relationship(
        "Message",
        backref="media",
        lazy=True
    )