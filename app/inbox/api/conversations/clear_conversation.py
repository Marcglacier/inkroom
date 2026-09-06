# app/inbox/api/conversations/clear_conversation.py

from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from app.inbox.services.conversations.lifecycle.clear_conversation_service import (
    ClearConversationService,
)


class ClearConversationAPI(MethodView):

    @jwt_required()
    def delete(
        self,
        conversation_id,
    ):

        user_id = int(get_jwt_identity())

        ClearConversationService(
            conversation_id=conversation_id,
            user_id=user_id,
        ).execute()

        return {
            "message": "Conversation cleared.",
        }, 200