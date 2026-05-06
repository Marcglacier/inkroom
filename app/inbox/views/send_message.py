# app/inbox/views/send_message.py

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

from app.inbox.services.message_service import MessageService


class SendMessageAPI(MethodView):

    @jwt_required()
    def post(self, user_id):

        sender_id = int(get_jwt_identity())

        data = request.get_json(silent=True) or {}
        content = data.get("content", "").strip()

        # -------------------------
        # VALIDATION
        # -------------------------
        if not content:
            return {"error": "Message content is required"}, 400

        # -------------------------
        # SEND MESSAGE
        # -------------------------
        result = MessageService.send_message(
            sender_id=sender_id,
            receiver_id=user_id,
            content=content
        )

        return result, 201