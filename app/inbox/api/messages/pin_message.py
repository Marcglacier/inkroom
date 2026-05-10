# app/inbox/views/pin_message.py
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.messages.pin_message import pin_message


class PinMessageAPI(MethodView):

    @jwt_required()
    def post(self, message_id):

        user_id = int(get_jwt_identity())

        result = pin_message(user_id, message_id)

        if isinstance(result, tuple):
            return result

        return result, 200