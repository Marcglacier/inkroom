# app/inbox/api/inbox/settings/read_receipt_settings.py
from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user import User
from app.extensions import db


class ReadReceiptSettingsAPI(MethodView):

    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())
        user = db.session.get(User, user_id)

        if user is None or user.is_deleted:
            return {"error": "User not found"}, 404

        return {
            "show_read_receipts": user.show_read_receipts,
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

        value = data.get("show_read_receipts")

        if not isinstance(value, bool):
            return {
                "error": "show_read_receipts must be a boolean"
            }, 400

        user.show_read_receipts = value
        db.session.commit()

        return {
            "show_read_receipts": user.show_read_receipts,
        }, 200