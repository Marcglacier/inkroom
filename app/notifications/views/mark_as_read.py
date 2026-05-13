# app/notifications/views/mark_as_read.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.notification import Notification


class MarkAsReadAPI(MethodView):

    @jwt_required()
    def patch(self, notification_id):

        user_id = int(get_jwt_identity())

        notification = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first()

        if not notification:
            return jsonify({"error": "Notification not found"}), 404

        notification.is_read = True
        db.session.commit()

        return jsonify({"message": "Marked as read"})