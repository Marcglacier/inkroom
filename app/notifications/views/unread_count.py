# app/notifications/views/get_notifications.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.notification import Notification


class UnreadCountAPI(MethodView):

    @jwt_required()
    def get(self):

        user_id = int(get_jwt_identity())

        count = Notification.query.filter_by(
            user_id=user_id,
            is_read=False
        ).count()

        return jsonify({
            "unread_count": count
        })