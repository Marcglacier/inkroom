# app/notifications/views/mark_all_as_read.py
from flask.views import MethodView
from flask import jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from app.notifications.services import (
    mark_all_as_read
)


class MarkAllAsReadAPI(MethodView):

    @jwt_required()
    def patch(self):

        user_id = int(get_jwt_identity())

        result = mark_all_as_read(user_id)

        return jsonify(result), 200