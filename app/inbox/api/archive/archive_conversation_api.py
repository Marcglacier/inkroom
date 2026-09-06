from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from app.inbox.services.archive.archive_conversation_service import (
    ArchiveConversationService,
)


class ArchiveConversationAPI(MethodView):

    decorators = [jwt_required()]

    def post(self, conversation_id):

        user_id = int(get_jwt_identity())

        ArchiveConversationService(
            user_id=user_id,
            conversation_id=conversation_id,
        ).execute()

        return jsonify({
            "message": "Conversation archived."
        }), 200