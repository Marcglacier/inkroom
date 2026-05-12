# app/inbox/api/search/search_conversation_api.py

from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.search.search_conversation_messages import search_conversation
from app.inbox.serializers.message_serializer import MessageSerializer


class SearchConversationAPI(MethodView):

    decorators = [jwt_required()]

    def get(self, conversation_id):

        user_id = get_jwt_identity()
        text = request.args.get("q", "")

        messages = search_conversation(user_id, conversation_id, text)

        return jsonify({
            "results": [
                MessageSerializer(m).to_dict()
                for m in messages
            ]
        }), 200