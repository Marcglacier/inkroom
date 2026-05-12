# app/inbox/views/react_to_message.py

from flask.views import MethodView
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.messages.react_to_message import toggle_reaction


class ReactToMessageAPI(MethodView):

    @jwt_required()
    def post(self, message_id):

        user_id = int(get_jwt_identity())

        # =========================
        # GET JSON SAFELY
        # =========================
        data = request.get_json(force=True, silent=True) or {}

        emoji = data.get("emoji")

        if isinstance(emoji, str):
            emoji = emoji.strip()

        print("RAW EMOJI:", repr(emoji))

        if not emoji:
            return {"error": "Emoji is required"}, 400

        # =========================
        # CALL SERVICE
        # =========================
        result = toggle_reaction(
            user_id=user_id,
            message_id=message_id,
            emoji=emoji
        )

        # =========================
        # HANDLE SERVICE RESPONSE
        # =========================
        if isinstance(result, tuple):
            return result

        return result, 200