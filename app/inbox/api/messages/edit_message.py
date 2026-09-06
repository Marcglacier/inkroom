# app/inbox/views/edit_message.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.inbox.services.messages.edit_message import (edit_message,)
from app.inbox.models.messages.message import Message
from datetime import datetime, timedelta


class EditMessageAPI(MethodView):

    @jwt_required()
    def put(self, message_id):

        user_id = int(get_jwt_identity())

        message = Message.query.get_or_404(message_id)

        if message.sender_id != user_id:
            return jsonify({"error": "Not allowed"}), 403

        data = request.get_json() or {}
        new_content = data.get("content", "").strip()
         
        if datetime.utcnow() - message.created_at > timedelta(minutes=20):
            return jsonify({ "error": "Editing period expired" }), 403
        
        if not new_content:
            return jsonify({"error": "Content required"}), 400

        if new_content == message.content:
            return jsonify({"error": "Nothing changed"}), 400
        
        payload = edit_message(message,new_content,)

        return jsonify(payload), 200