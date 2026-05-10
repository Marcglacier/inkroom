# app/inbox/views/fetch_pinned_messages.py
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from app.inbox.services.messages.fetch_pinned_messages import fetch_pinned


class FetchPinnedMessagesAPI(MethodView):

    @jwt_required()
    def get(self, conversation_id):

        results = fetch_pinned(conversation_id)

        return results, 200