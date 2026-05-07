# app/inbox/views/delete_message.py

from datetime import datetime

from flask.views import MethodView
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.inbox.models.message import Message


class DeleteMessageAPI(MethodView):

    @jwt_required()
    def delete(self, message_id):

        user_id = int(get_jwt_identity())
        message = Message.query.get_or_404(message_id)

        data = request.get_json(silent=True) or {}
        mode = data.get("mode", "me")

        # =========================
        # SECURITY
        # =========================
        if mode == "everyone" and message.sender_id != user_id:
            return jsonify({"error": "Only sender can delete for everyone"}), 403

        if message.deleted_for_everyone:
            return jsonify({"error": "Already deleted for everyone"}), 400

        message.delete_requested_at = datetime.utcnow()

        # =========================
        # DELETE FOR EVERYONE
        # =========================
        if mode == "everyone":
            message.deleted_for_everyone = True

        # =========================
        # DELETE FOR ME
        # =========================
        elif mode == "me":
            deleted_users = message.deleted_for_users or []

            if user_id not in deleted_users:
                deleted_users.append(user_id)

            message.deleted_for_users = deleted_users

        else:
            return jsonify({"error": "Invalid mode"}), 400

        db.session.commit()

        return jsonify({
            "message": "Delete scheduled",
            "message_id": message.id,
            "mode": mode
        })