# app/inbox/models/calls/call.py

from datetime import datetime

from app.extensions import db


class Call(db.Model):
    __tablename__ = "calls"

    # ============================================================
    # CORE
    # ============================================================

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "conversations.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    caller_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    # ============================================================
    # CALL
    # ============================================================

    call_type = db.Column(
        db.String(20),
        nullable=False,
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="calling",
        index=True,
    )

    # ============================================================
    # TIMESTAMPS
    # ============================================================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    started_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    answered_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    ended_at = db.Column(
        db.DateTime,
        nullable=True,
    )

    # ============================================================
    # RELATIONSHIPS
    # ============================================================

    conversation = db.relationship(
        "Conversation",
        backref="calls",
    )

    caller = db.relationship(
        "User",
        foreign_keys=[caller_id],
    )

    receiver = db.relationship(
        "User",
        foreign_keys=[receiver_id],
    )

    # ============================================================
    # REPRESENTATION
    # ============================================================

    def __repr__(self):
        return (
            f"<Call {self.id} "
            f"type={self.call_type} "
            f"status={self.status} "
            f"caller={self.caller_id} "
            f"receiver={self.receiver_id}>"
        )