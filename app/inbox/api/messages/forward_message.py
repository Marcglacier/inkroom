# app/inbox/views/forward_message.py
from flask.views import MethodView
from flask import request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from app.inbox.services.messages.forward_message import (
    forward_message,
)


class ForwardMessageAPI(MethodView):

    @jwt_required()
    def post(self):

        sender_id = int(get_jwt_identity())

        data = request.get_json() or {}

        message_id = data.get("message_id")
        to_user_id = data.get("to_user_id")

        if not message_id or not to_user_id:
            return {
                "error": "message_id and to_user_id required"
            }, 400

        response, status = forward_message(
            sender_id,
            message_id,
            to_user_id,
        )

        return response, status