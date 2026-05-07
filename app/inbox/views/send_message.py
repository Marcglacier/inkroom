# app/inbox/views/send_message.py

from flask.views import MethodView
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.messages.send_message import send_message


class SendMessageAPI(MethodView):

    @jwt_required()
    def post(self, user_id):

        sender_id = int(get_jwt_identity())

        data = request.get_json(silent=True) or {}
        content = data.get("content", "").strip()

        if not content:
            return {"error": "Message content is required"}, 400

        result = send_message(
            sender_id=sender_id,
            receiver_id=user_id,
            content=content
        )

        return result, 201