# app/notifications/views/settings.py
from flask.views import MethodView
from flask import jsonify, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from app.notifications.services.settings.notification_settings_service import (
    notification_settings_service,
)


class NotificationSettingsAPI(MethodView):

    @jwt_required()
    def get(self):

        user_id = int(get_jwt_identity())

        result = notification_settings_service.get(
            user_id
        )

        return jsonify(result), 200

    @jwt_required()
    def post(self):

        user_id = int(get_jwt_identity())

        data = request.get_json(silent=True) or {}

        duration = data.get("duration")

        if not duration:
            return jsonify({
                "error": "duration is required"
            }), 400

        try:
            result = notification_settings_service.mute(
                user_id,
                duration,
            )

        except ValueError as error:
            return jsonify({
                "error": str(error)
            }), 400

        return jsonify(result), 200

    @jwt_required()
    def delete(self):

        user_id = int(get_jwt_identity())

        result = notification_settings_service.unmute(
            user_id
        )

        return jsonify(result), 200