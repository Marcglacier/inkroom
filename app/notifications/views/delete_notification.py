# app/notifications/views/delete_notification.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.notification import Notification


class DeleteNotificationAPI(MethodView):

    @jwt_required()
    def delete(self, notification_id):

        user_id = int(get_jwt_identity())

        notif = Notification.query.filter_by(
            id=notification_id,
            user_id=user_id
        ).first()

        if not notif:
            return jsonify({"error": "Notification not found"}), 404

        db.session.delete(notif)
        db.session.commit()

        return jsonify({"message": "Notification deleted"})