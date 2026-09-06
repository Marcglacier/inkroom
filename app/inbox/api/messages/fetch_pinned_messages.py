# app/inbox/api/messages/fetch_pinned_messages.py


from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.messages.fetch_pinned_messages import fetch_pinned


class FetchPinnedMessagesAPI(MethodView):

    @jwt_required()
    def get(self, conversation_id):

        user_id = int(get_jwt_identity())

        results = fetch_pinned(
            conversation_id,
            user_id,
        )

        return results, 200