# app/inbox/api/inbox/open_link.py
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.links.open_link import (
    OpenLinkService,
)


class OpenLinkAPI(MethodView):

    @jwt_required()
    def post(self, link_id):

        result = OpenLinkService(
            user_id=int(get_jwt_identity()),
            link_id=link_id,
        ).execute()

        return result, 200