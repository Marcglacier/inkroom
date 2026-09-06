# app/inbox/views/conversations/conversation_mute_api.py

from flask import request
from flask.views import MethodView

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from app.inbox.services.conversations.mutes.mute_conversation_service import (
    MuteConversationService,
)


class MuteConversationAPI(MethodView):

    @jwt_required()
    def post(
        self,
        conversation_id: int,
    ):
        user_id = int(get_jwt_identity())

        duration = request.json.get("duration")

        MuteConversationService(
            conversation_id=conversation_id,
            user_id=user_id,
            duration=duration,
        ).execute()

        return {
            "message": "Conversation muted.",
        }, 200