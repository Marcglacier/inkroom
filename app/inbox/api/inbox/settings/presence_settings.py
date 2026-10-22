# app/inbox/api/inbox/settings/presence_settings.py
from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user import User
from app.extensions import db
from app.inbox.services.presence.presence_events import (
    emit_presence_snapshot,
    emit_presence_status,
)
from app.sockets.presence_store import online_users, last_seen

class PresenceSettingsAPI(MethodView):

    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if user is None or user.is_deleted:
            return {"error": "User not found"}, 404

        return {
            "show_online_status": user.show_online_status,
        }, 200

    @jwt_required()
    def patch(self):
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if user is None or user.is_deleted:
            return {"error": "User not found"}, 404

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return {"error": "A JSON object is required"}, 400

        value = data.get("show_online_status")

        if not isinstance(value, bool):
            return {
                "error": "show_online_status must be a boolean"
            }, 400

        user.show_online_status = value
        db.session.commit()

        # Refresh what this user can see.
        emit_presence_snapshot(user_id)

        # Refresh how other users see this user.
        emit_presence_status(
            user_id=user_id,
            online=online_users.get(user_id, False),
            last_seen=last_seen.get(user_id),
        )

        return {
            "show_online_status": user.show_online_status,
        }, 200