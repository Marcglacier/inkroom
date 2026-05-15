# app/notifications/views/delete_notification.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.notification import Notification


class DeleteReadNotificationsAPI(MethodView):

    @jwt_required()
    def delete(self):

        user_id = int(get_jwt_identity())

        deleted = Notification.query.filter_by(
            user_id=user_id,
            is_read=True
        ).delete()

        db.session.commit()

        return jsonify({
            "message": "Read notifications deleted",
            "deleted": deleted
        })