from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.conversations.lifecycle.mark_conversation_read import (
    MarkConversationReadService,
)


class MarkConversationReadAPI(MethodView):

    def __init__(self):
        self.service = MarkConversationReadService()

    @jwt_required()
    def post(self, conversation_id):
        user_id = int(get_jwt_identity())
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return {"error": "A JSON object is required"}, 400

        through_message_id = data.get("through_message_id")

        if (
            isinstance(through_message_id, bool)
            or not isinstance(through_message_id, (int, str))
            or not str(through_message_id).isdigit()
            or int(through_message_id) <= 0
        ):
            return {
                "error": "through_message_id must be a positive integer"
            }, 400

        last_read_message_id = self.service.execute(
            conversation_id=conversation_id,
            user_id=user_id,
            through_message_id=int(through_message_id),
        )

        return {
            "success": True,
            "last_read_message_id": last_read_message_id,
        }, 200
