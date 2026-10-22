# app/inbox/api/messages/delete_message.py

from flask.views import MethodView
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.inbox.services.messages.delete_message import (delete_for_me, delete_for_everyone,)
from app.inbox.models.messages.message import Message
from app.inbox.services.settings.blocks.block_policy import BlockPolicy
from app.inbox.models.conversations.conversation_participant import ConversationParticipant

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

        if mode == "everyone" and message.deleted_for_everyone:
            return jsonify({"error": "Already deleted for everyone"}), 400

        if message.conversation_id:
            participants = ConversationParticipant.query.filter_by(
                conversation_id=message.conversation_id
            ).all()

            other_ids = {
                p.user_id
                for p in participants
                if p.user_id is not None and p.user_id != user_id
            }

            if any(
                BlockPolicy.blocks_either_user(user_id, other_id)
                for other_id in other_ids
            ):
                return jsonify({
                    "error": "Message deletion is unavailable"
                }), 403


        # =========================
        # DELETE
        # =========================
        if mode == "everyone":
           delete_for_everyone(message)

        elif mode == "me":
           delete_for_me(message, user_id)

        else:
         return jsonify({"error": "Invalid mode"}), 400

        return jsonify({
          "message": "Delete scheduled",
          "message_id": message.id,
          "mode": mode,
        })