# app/inbox/views/unpin_message.py
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.inbox.services.messages.unpin_message import unpin_message


class UnpinMessageAPI(MethodView):

    @jwt_required()
    def delete(self, message_id):

        user_id = int(get_jwt_identity())
        result = unpin_message(user_id, message_id)

        if isinstance(result, tuple):
            return result

        return result, 200