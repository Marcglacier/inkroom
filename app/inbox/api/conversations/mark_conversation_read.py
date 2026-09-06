from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.conversations.lifecycle.mark_conversation_read import mark_conversation_read


class MarkConversationReadAPI(MethodView):

    @jwt_required()
    def post(self, conversation_id):
        user_id = int(get_jwt_identity())

        mark_conversation_read(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        return {"success": True}, 200