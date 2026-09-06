# app/inbox/views/conversations/unmute_conversation_api.py
from flask.views import MethodView

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from app.inbox.services.conversations.mutes.unmute_conversation_service import (
    UnmuteConversationService,
)


class UnmuteConversationAPI(MethodView):

    @jwt_required()
    def delete(
        self,
        conversation_id: int,
    ):
        user_id = int(get_jwt_identity())

        UnmuteConversationService(
            conversation_id=conversation_id,
            user_id=user_id,
        ).execute()

        return {
            "message": "Conversation unmuted.",
        }, 200