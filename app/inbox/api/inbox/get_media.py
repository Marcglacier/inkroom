from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.inbox.services.media.get_archive_media import (
    get_archive_media,
)


class GetArchiveMediaAPI(MethodView):

    @jwt_required()
    def get(self, conversation_id):

        media = get_archive_media(
            int(get_jwt_identity()),
            conversation_id,
        )

        return {
            "media": media,
        }, 200