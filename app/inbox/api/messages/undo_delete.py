# app/inbox/views/undo_delete.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.inbox.services.messages.delete_message import undo_delete
from datetime import datetime, timedelta

from app.extensions import db
from app.inbox.models.message import Message

class UndoDeleteAPI(MethodView):

    @jwt_required()
    def post(self, message_id):

        user_id = int(get_jwt_identity())
        message = Message.query.get_or_404(message_id)

        # only allow undo within 10 seconds
        if not message.delete_requested_at:
            return jsonify({"error": "Nothing to undo"}), 400

        if datetime.utcnow() - message.delete_requested_at > timedelta(seconds=10):
            return jsonify({"error": "Undo window expired"}), 400

        # restore
        undo_delete(message, user_id)

        return jsonify({
            "message": "Message restored",
            "message_id": message.id
        })