# app/inbox/api/inbox/get_archive_links.py
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.links.get_archive_links import (
    GetArchiveLinksService,
)


class GetArchiveLinksAPI(MethodView):

    @jwt_required()
    def get(self, conversation_id):

        links = GetArchiveLinksService(
            user_id=int(get_jwt_identity()),
            conversation_id=conversation_id,
        ).execute()

        return {
            "links": links,
        }, 200