# app/inbox/api/archive/get_archived_conversations_api.py
from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import ( jwt_required, get_jwt_identity, )
from app.inbox.services.archive.get_archived_conversations_service import (
     GetArchivedConversationsService, )


class GetArchivedConversationsAPI(MethodView):

    decorators = [jwt_required()]

    def get(self):

        user_id = int(get_jwt_identity())

        conversations = (
            GetArchivedConversationsService(
                user_id=user_id,
            ).execute()
        )

        return jsonify({
            "conversations": conversations,
        }), 200