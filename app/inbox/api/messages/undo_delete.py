# app/inbox/api/messages/undo_delete.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.inbox.services.messages.delete_message import undo_delete
from datetime import datetime, timedelta
from app.inbox.models.conversations.conversation_participant import ConversationParticipant
from app.inbox.services.settings.blocks.block_policy import BlockPolicy
from app.extensions import db
from app.inbox.models.messages.message import Message

class UndoDeleteAPI(MethodView):

    @jwt_required()
    def post(self, message_id):

        user_id = int(get_jwt_identity())
        message = Message.query.get_or_404(message_id)
        # Only the original sender can undo deletion for everyone.
        if message.sender_id != user_id:
            return jsonify({"error": "Not allowed"}), 403

        if not message.deleted_for_everyone:
            return jsonify({"error": "Message is not deleted"}), 400

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
                    "error": "Message restoration is unavailable"
                }), 403

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