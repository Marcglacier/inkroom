from flask.views import MethodView

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.extensions import db

from app.inbox.models.conversations.conversation import Conversation
from app.inbox.models.conversations.conversation_request import (
    ConversationRequest
)


class RejectRequestAPI(MethodView):

    @jwt_required()
    def post(self, conversation_id):

        current_user = int(
            get_jwt_identity()
        )

        request = (
            ConversationRequest.query
            .filter_by(
                conversation_id=conversation_id,
                receiver_id=current_user
            )
            .first()
        )

        if not request:

            return {
                "error": "Request not found"
            }, 404

        conversation = (
            Conversation.query
            .get(conversation_id)
        )

        if not conversation:

            return {
                "error": "Conversation not found"
            }, 404

        print(
            "\n🔥 REJECTING REQUEST"
        )

        print(
            "CONVERSATION:",
            conversation.id
        )

        print(
            "SENDER:",
            request.sender_id
        )

        print(
            "RECEIVER:",
            request.receiver_id
        )

        conversation.status = "rejected"

        request.status = "rejected"

        db.session.commit()

        print(
            "✅ REQUEST MARKED REJECTED"
        )

        return {
            "message": "Request rejected"
        }, 200