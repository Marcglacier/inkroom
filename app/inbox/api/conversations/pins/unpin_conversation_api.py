# app/inbox/api/conversations/unpin_conversation_api.py

from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from app.inbox.services.conversations.pins.unpin_conversation_service import (
    UnpinConversationService,
)


class UnpinConversationAPI(MethodView):

    @jwt_required()
    def delete(self, conversation_id):

        user_id = int(get_jwt_identity())

        UnpinConversationService(
            conversation_id=conversation_id,
            user_id=user_id,
        ).execute()

        return {
            "message": "Conversation unpinned.",
        }, 200