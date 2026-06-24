from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.inbox.models.conversation import Conversation
from app.inbox.models.message import Message

from app.models.user import User
from app.models.profile import Profile


class RequestConversationAPI(MethodView):

    @jwt_required()
    def get(self, conversation_id):

        current_user = int(
            get_jwt_identity()
        )

        conversation = (
            Conversation.query
            .get_or_404(conversation_id)
        )

        if conversation.status != "pending":

            return {
                "error": "Not a request"
            }, 400

        participant_ids = [

            p.user_id

            for p in conversation.participants

        ]

        if current_user not in participant_ids:

            return {
                "error": "Forbidden"
            }, 403

        sender_id = next(

            pid

            for pid in participant_ids

            if pid != current_user

        )

        sender = User.query.get(
            sender_id
        )

        profile = (
            Profile.query
            .filter_by(
                user_id=sender.id
            )
            .first()
        )

        messages = (

            Message.query

            .filter_by(
                conversation_id=conversation.id
            )

            .order_by(
                Message.created_at.asc()
            )

            .all()

        )

        return {

            "conversation_id":
                conversation.id,

            "sender": {

                "id":
                    sender.id,

                "name":
                    sender.name,

                "username":
                    sender.username,

                "avatar":
                    profile.avatar_url
                    if profile
                    else None

            },

            "messages": [

                {

                    "id":
                        m.id,

                    "content":
                        m.content,

                    "sender_id":
                        m.sender_id,

                    "created_at":
                        m.created_at.isoformat()

                }

                for m in messages

            ]

        }, 200