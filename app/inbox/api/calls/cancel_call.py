# app/inbox/api/calls/cancel_call.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.calls.cancel_call_service import (
    CancelCallService,
)
from app.inbox.serializers.call_serializer import CallSerializer


class CancelCallAPI(MethodView):

    @jwt_required()
    def post(self, call_id):

        user_id = int(get_jwt_identity())

        call = CancelCallService(
            call_id=call_id,
            user_id=user_id,
        ).execute()

        return jsonify({
            "call": CallSerializer(call).to_dict(),
        }), 200