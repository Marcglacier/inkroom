# app/inbox/services/archive/restore_conversation_service.py
from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import ( jwt_required, get_jwt_identity, )

from app.inbox.services.archive.restore_conversation_service import ( RestoreConversationService, )


class RestoreConversationAPI(MethodView):

    decorators = [jwt_required()]

    def delete(self, conversation_id):

        user_id = int(get_jwt_identity())

        RestoreConversationService(
            user_id=user_id,
            conversation_id=conversation_id,
        ).execute()

        return jsonify({
            "message": "Conversation restored."
        }), 200
