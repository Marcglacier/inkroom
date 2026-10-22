from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.inbox.models.conversations.conversation_request import (
    ConversationRequest
)

from app.inbox.models.messages.message import Message

from app.models.user import User
from app.models.profile import Profile
from app.models.settings.user_restriction import UserRestriction
from app.inbox.models.conversations.conversation import Conversation
from app.inbox.models.conversations.conversation_participant import (
    ConversationParticipant,
)
from app.storage.service import get_file_url
from app.inbox.models.conversations.conversation_hide import (
    ConversationHide,
)

class ListRequestsAPI(MethodView):

    @jwt_required()
    def get(self):

        current_user = int( get_jwt_identity() )

        requests = (

            ConversationRequest.query
            .filter_by( receiver_id=current_user )
            .order_by( ConversationRequest.created_at.desc() )
            .all()

        )

        print("\n========== REQUEST DEBUG ==========")
        print("CURRENT USER:", current_user)
        print("REQUESTS FOUND:", len(requests))

        for req in requests:

            print(
                "CONVO:",
                req.conversation_id,
                "| SENDER:",
                req.sender_id,
                "| RECEIVER:",
                req.receiver_id
            )

        print("===================================\n")

        data = []

        for request in requests:

            sender = User.query.get(
                request.sender_id
            )

            profile = (
                Profile.query
                .filter_by(
                    user_id=sender.id
                )
                .first()
            )

            last_message = (
                Message.query
                .filter_by(
                    conversation_id=request.conversation_id
                )
                .order_by(
                    Message.created_at.desc()
                )
                .first()
            )

            data.append({

                "conversation_id":  request.conversation_id,
                "user_id": sender.id,
                "name": sender.name,
                "username": sender.username,
                "avatar": (
                    get_file_url(sender.profile_picture)
                    if sender and sender.profile_picture and not sender.is_deleted
                    else None
                ),
                "preview": last_message.content if last_message else "Sent a request",
                "status": request.status
            })
        restrictions = UserRestriction.query.filter_by(
            restricter_id=current_user,
        ).all()

        for restriction in restrictions:
            conversation = Conversation.find_between_users(
                current_user,
                restriction.restricted_id,
            )

            if not conversation or conversation.status != "active":
                continue

            hidden = ConversationHide.query.filter_by(
                conversation_id=conversation.id,
                user_id=current_user,
            ).first()

            if hidden:
                latest_message = (
                    Message.query
                    .filter_by(conversation_id=conversation.id)
                    .order_by(Message.created_at.desc())
                    .first()
                )

                # Keep the deleted chat hidden until a newer message arrives.
                if not latest_message or latest_message.created_at <= hidden.hidden_at:
                    continue

            # Skip conversations already represented by a real request.
            if any(
                item["conversation_id"] == conversation.id
                for item in data
            ):
                continue

            other_user = User.query.get(restriction.restricted_id)
            if not other_user:
                continue

            profile = Profile.query.filter_by(
                user_id=other_user.id,
            ).first()

            last_message = (
                Message.query
                .filter_by(conversation_id=conversation.id)
                .order_by(Message.created_at.desc())
                .first()
            )

            data.append({
                "conversation_id": conversation.id,
                "user_id": other_user.id,
                "name": other_user.name,
                "username": other_user.username,
                "avatar": (
                    get_file_url(other_user.profile_picture)
                    if other_user.profile_picture and not other_user.is_deleted
                    else None
                ),
                "preview": (
                    last_message.content
                    if last_message
                    else "Restricted conversation"
                ),
                "status": "restricted",
                "type": "restricted",
            })

        return data, 200