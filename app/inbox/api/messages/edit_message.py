# app/inbox/views/edit_message.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.inbox.models.message import Message


class EditMessageAPI(MethodView):

    @jwt_required()
    def put(self, message_id):

        user_id = int(get_jwt_identity())

        message = Message.query.get_or_404(message_id)

        if message.sender_id != user_id:
            return jsonify({"error": "Not allowed"}), 403

        data = request.get_json() or {}
        new_content = data.get("content", "").strip()

        if not new_content:
            return jsonify({"error": "Content required"}), 400

        message.content = new_content
        message.edited = True

        db.session.commit()

        return jsonify({
            "message": "updated",
            "id": message.id,
            "content": message.content,
            "edited": True
        }), 200