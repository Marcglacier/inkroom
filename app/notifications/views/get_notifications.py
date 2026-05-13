# app/notifications/views/get_notifications.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.notification import Notification


class GetNotificationsAPI(MethodView):

    @jwt_required()
    def get(self):

        user_id = int(get_jwt_identity())

        notifications = Notification.query.filter_by(
            user_id=user_id
        ).order_by(
            Notification.created_at.desc()
        ).limit(50).all()

        return jsonify([
            n.to_dict() for n in notifications
        ])