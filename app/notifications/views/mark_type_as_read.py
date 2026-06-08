# app/notifications/views/mark_type_as_read.py
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

from app.notifications.services.actions.mark_type_as_read import mark_type_as_read


class MarkTypeAsReadAPI(MethodView):

    @jwt_required()
    def post(self, notification_type):

        user_id = int(get_jwt_identity())

        try:
            result = mark_type_as_read(user_id, notification_type)

            return jsonify({
                "success": True,
                "data": result
            }), 200

        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500