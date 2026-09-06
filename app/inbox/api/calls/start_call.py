# app/inbox/api/calls/start_call.py

from flask.views import MethodView
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.calls.start_call_service import (
    StartCallService,
)
from app.inbox.serializers.call_serializer import CallSerializer


class StartCallAPI(MethodView):

    @jwt_required()
    def post(self):

        user_id = int(get_jwt_identity())

        data = request.get_json(silent=True) or {}

        call = StartCallService(
            conversation_id=data.get("conversation_id"),
            user_id=user_id,
            call_type=data.get("call_type"),
        ).execute()

        return jsonify({
            "call": CallSerializer(call).to_dict(),
        }), 201