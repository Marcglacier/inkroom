# app/inbox/api/conversations/pins/pin_conversation_api.py

from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from app.inbox.services.conversations.pins.pin_conversation import (
    PinConversationService,
)


class PinConversationAPI(MethodView):

    @jwt_required()
    def post(self, conversation_id):

        user_id = int(get_jwt_identity())

        PinConversationService(
            conversation_id=conversation_id,
            user_id=user_id,
        ).execute()

        return {
            "message": "Conversation pinned.",
        }, 200