from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.conversations.core.fetch_message_context import (
    FetchMessageContextService,
)
from app.inbox.services.conversations.core.conversation_guard import (
    ConversationGuard,
)

class MessageContextAPI(MethodView):
    decorators = [jwt_required()]

    def get(self, conversation_id, message_id):
        user_id = int(get_jwt_identity())
        ConversationGuard.require_participant(conversation_id, user_id)

        result = FetchMessageContextService(
            conversation_id=conversation_id,
            message_id=message_id,
            user_id=user_id,
        ).execute()

        if result is None:   
            return {
                "message": "Message not found."
            }, 404

        return {
          "messages": result
        }, 200