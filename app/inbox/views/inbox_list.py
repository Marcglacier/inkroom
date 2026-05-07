# app/inbox/views/inbox_list.py

from datetime import datetime

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.inbox.models.message import Message
from app.inbox.services.inbox.get_inbox import get_inbox


class InboxAPI(MethodView):

    @jwt_required()
    def get(self):

        user_id = int(get_jwt_identity())

        # ==================================
        # MARK RECEIVED MESSAGES AS DELIVERED
        # ==================================
        (
            Message.query
            .filter(
                Message.sender_id != user_id,
                Message.delivered_at.is_(None)
            )
            .update(
                {
                    Message.delivered_at: datetime.utcnow(),
                    Message.status: "delivered"
                },
                synchronize_session=False
            )
        )

        db.session.commit()

        # ==================================
        # FETCH USER INBOX
        # (service handles hidden conversations)
        # ==================================
        inbox = get_inbox(user_id)

        return inbox, 200