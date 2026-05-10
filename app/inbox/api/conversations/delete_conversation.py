# app/inbox/views/delete_conversation.py
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

from app.inbox.services.conversations.delete_conversation import delete_conversation


class DeleteConversationAPI(MethodView):

    @jwt_required()
    def delete(self, conversation_id):

        user_id = int(get_jwt_identity())

        result = delete_conversation(
            conversation_id,
            user_id
        )

        return jsonify(result)