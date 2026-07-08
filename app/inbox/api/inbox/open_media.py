from flask.views import MethodView
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from app.inbox.services.media.open_media import open_media


class OpenMediaAPI(MethodView):

    @jwt_required()
    def post(self, media_id):

        result = open_media(
            int(get_jwt_identity()),
            media_id,
        )

        return result, 200