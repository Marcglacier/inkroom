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


class ListRequestsAPI(MethodView):

    @jwt_required()
    def get(self):

        current_user = int(
            get_jwt_identity()
        )

        requests = (

            ConversationRequest.query

            .filter_by(
                receiver_id=current_user
            )

            .order_by(
                ConversationRequest.created_at.desc()
            )

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

    "conversation_id":
        request.conversation_id,

    "user_id":
        sender.id,

    "name":
        sender.name,

    "username":
        sender.username,

    "avatar":
        profile.avatar_url
        if profile
        else None,

    "preview":
        last_message.content
        if last_message
        else "Sent a request",

    "status":
        request.status

})

        return data, 200