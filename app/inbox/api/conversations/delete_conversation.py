# app/inbox/views/delete_conversation.py

from flask import jsonify
from flask.views import MethodView

from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from app.inbox.services.conversations.lifecycle.delete_conversation_service import (
    DeleteConversationService,
)


class DeleteConversationAPI(MethodView):

    decorators = [jwt_required()]

    def delete(
        self,
        conversation_id,
    ):

        user_id = int(get_jwt_identity())

        result = DeleteConversationService(
            conversation_id=conversation_id,
            user_id=user_id,
        ).execute()

        return jsonify(result), 200