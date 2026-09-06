# app/inbox/api/calls/end_call.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.calls.end_call_service import (
    EndCallService,
)
from app.inbox.serializers.call_serializer import CallSerializer


class EndCallAPI(MethodView):

    @jwt_required()
    def post(self, call_id):

        user_id = int(get_jwt_identity())

        call = EndCallService(
            call_id=call_id,
            user_id=user_id,
        ).execute()

        return jsonify({
            "call": CallSerializer(call).to_dict(),
        }), 200