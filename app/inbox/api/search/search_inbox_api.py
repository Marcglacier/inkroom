# app/inbox/api/search/search_inbox_api.py
from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.inbox.services.search.search_inbox import search_inbox


class SearchInboxAPI(MethodView):

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()
        text = request.args.get("q")

        if not text:
            return jsonify({"error": "Search query required"}), 400

        results = search_inbox(user_id, text)

        formatted = []

        for r in results:
            formatted.append({
                "conversation_id": r.conversation_id,
                "username": r.sender.username if hasattr(r, "sender") else None,
                "last_message": r.content,
                "last_message_time": r.created_at,
                "message_id": r.id,
                "sender_id": r.sender_id
            })

        return jsonify({
            "results": formatted
        }), 200