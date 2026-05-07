# app/inbox/views/inbox_list.py

from datetime import datetime

from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from sqlalchemy import func

from app.extensions import db
from app.inbox.models.conversation import Conversation
from app.inbox.models.conversation_participant import (
    ConversationParticipant
)
from app.inbox.models.message import Message
from app.models.user import User


class InboxAPI(MethodView):

    @jwt_required()
    def get(self):

        current_user = int(
            get_jwt_identity()
        )

        participations = (
            ConversationParticipant.query
            .filter_by(user_id=current_user)
            .all()
        )

        results = []

        for p in participations:

            convo = Conversation.query.get(
                p.conversation_id
            )

            if not convo:
                continue

            # -------------------------
            # FIND OTHER PARTICIPANT
            # -------------------------
            other = (
                ConversationParticipant.query
                .filter(
                    ConversationParticipant.conversation_id == convo.id,
                    ConversationParticipant.user_id != current_user
                )
                .first()
            )

            if not other:
                continue

            other_user = User.query.get(
                other.user_id
            )

            if not other_user:
                continue

            # -------------------------
            # MARK AS DELIVERED
            # inbox fetch means
            # recipient received message
            # -------------------------
            Message.query.filter(
                Message.conversation_id == convo.id,
                Message.sender_id != current_user,
                Message.delivered_at.is_(None)
            ).update(
                {
                    "delivered_at": datetime.utcnow(),
                    "status": "delivered"
                },
                synchronize_session=False
            )

            db.session.commit()

            # -------------------------
            # LAST MESSAGE
            # -------------------------
            last_message = (
                Message.query
                .filter(
                    Message.conversation_id == convo.id,
                    Message.deleted_for_everyone.is_(False)
                )
                .order_by(Message.created_at.desc())
                .first()
            )

            last_message_content = (
                last_message.content
                if last_message
                else None
            )

            # -------------------------
            # UNREAD COUNT
            # -------------------------
            unread_count = (
                Message.query
                .with_entities(func.count())
                .filter(
                    Message.conversation_id == convo.id,

                    # not my own message
                    Message.sender_id != current_user,

                    # not opened/read yet
                    Message.read_at.is_(None),

                    # ignore deleted-for-everyone
                    Message.deleted_for_everyone.is_(False)
                )
                .scalar()
            )

            results.append({
                "conversation_id": convo.id,
                "user_id": other_user.id,
                "username": other_user.username,
                "last_message": last_message_content,
                "unread": unread_count
            })

        return results, 200