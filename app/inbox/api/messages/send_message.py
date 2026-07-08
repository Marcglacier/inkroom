# app/inbox/api/messages/send_message.py

from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.messages.send_message import send_message


class SendMessageAPI(MethodView):

    @jwt_required()
    def post(self, user_id):

        sender_id = int(get_jwt_identity())

        if request.content_type and request.content_type.startswith(
            "multipart/form-data"
        ):
            content = request.form.get("content")
            reply_to = request.form.get("reply_to_message_id")
            media_kind = request.form.get("media_kind")
            files = request.files.getlist("files")

        else:
            data = request.get_json(silent=True) or {}

            content = data.get("content")
            reply_to = data.get("reply_to_message_id")
            media_kind = None
            files = []

        result = send_message(
            sender_id=sender_id,
            receiver_id=int(user_id),
            content=content,
            files=files,
            reply_to_message_id=reply_to,
            media_kind=media_kind,
        )

        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]

        return jsonify(result), 201