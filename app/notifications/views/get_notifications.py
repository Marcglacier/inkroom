# app/notifications/views/get_notifications.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.notifications.services.readers.get_notifications import get_notifications


class GetNotificationsAPI(MethodView):

    @jwt_required()
    def get(self):

        user_id = int(get_jwt_identity())

        data = get_notifications(user_id)

        return jsonify({
            "notifications": data
        })