# app/notifications/views/unread_groups.py

from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from app.notifications.services.queries.get_unread_groups import (
    get_unread_groups_service,
)


class UnreadGroupsAPI(MethodView):

    @jwt_required()
    def get(self):

        user_id = int(get_jwt_identity())

        groups = get_unread_groups_service.get(user_id)

        return jsonify(groups), 200