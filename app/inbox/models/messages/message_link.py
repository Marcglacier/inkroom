# app/inbox/models/messages/message_link.py

from datetime import datetime

from app.extensions import db


class MessageLink(db.Model):
    __tablename__ = "message_links"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    message_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "messages.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    # ================= LINK =================

    url = db.Column(
        db.Text,
        nullable=False,
    )

    normalized_url = db.Column(
        db.Text,
        nullable=False,
        index=True,
    )

    # ================= PREVIEW =================

    title = db.Column(
        db.Text,
        nullable=True,
    )

    description = db.Column(
        db.Text,
        nullable=True,
    )

    image_url = db.Column(
        db.Text,
        nullable=True,
    )

    site_name = db.Column(
        db.String(255),
        nullable=True,
    )

    domain = db.Column(
        db.String(255),
        nullable=True,
    )

    # e.g. youtube, instagram, tiktok, facebook, x, generic
    platform = db.Column(
        db.String(50),
        nullable=True,
    )

    # e.g. video, article, social, image, generic
    content_type = db.Column(
        db.String(50),
        nullable=True,
    )

    fetched_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # ================= RELATIONSHIP =================

    message = db.relationship(
        "Message",
        back_populates="links",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "message_id": self.message_id,
            "sender_id": self.message.sender_id,
            "url": self.url,

            "title": self.title,
            "description": self.description,
            "image_url": self.image_url,

            "site_name": self.site_name,
            "domain": self.domain,
            "platform": self.platform,
            "content_type": self.content_type,

            "fetched_at": (
                self.fetched_at.isoformat() + "Z"
                if self.fetched_at
                else None
            ),

            "created_at": (
                self.created_at.isoformat() + "Z"
                if self.created_at
                else None
            ),
        }