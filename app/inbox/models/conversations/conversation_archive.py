from app.extensions import db


class ConversationArchive(db.Model):

    __tablename__ = "conversation_archives"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    archived_at = db.Column(
        db.DateTime,
        server_default=db.func.now(),
        nullable=False,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "conversation_id",
            name="uq_user_conversation_archive",
        ),
    )