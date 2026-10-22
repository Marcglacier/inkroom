# app/inbox/api/inbox/settings/actions/restrictions.py

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.user import User
from app.inbox.services.settings.restriction_service import (
    RestrictionService,
)


class RestrictionsAPI(MethodView):
    def __init__(self):
        self.service = RestrictionService()

    def _target_exists(self, current_id, target_id):
        current = db.session.get(User, current_id)
        target = db.session.get(User, target_id)

        return (
            current is not None
            and not current.is_deleted
            and target is not None
            and not target.is_deleted
        )


    @jwt_required()
    def get(self, user_id):
        current_id = int(get_jwt_identity())

        if current_id == user_id:
            return {"error": "Invalid restriction target"}, 400

        if not self._target_exists(current_id, user_id):
            return {"error": "User not found"}, 404

        restricted = self.service.is_restricted(
            current_id,
            user_id,
        )

        return {
            "user_id": user_id,
            "restricted": restricted,
        }, 200


    @jwt_required()
    def post(self, user_id):
        current_id = int(get_jwt_identity())

        if current_id == user_id:
            return {"error": "You cannot restrict yourself"}, 400

        if not self._target_exists(current_id, user_id):
            return {"error": "User not found"}, 404

        created = self.service.restrict(current_id, user_id)

        return {
            "user_id": user_id,
            "restricted": True,
        }, 201 if created else 200

    @jwt_required()
    def delete(self, user_id):
        current_id = int(get_jwt_identity())

        if current_id == user_id:
            return {"error": "Invalid restriction target"}, 400

        if not self._target_exists(current_id, user_id):
            return {"error": "User not found"}, 404

        self.service.unrestrict(current_id, user_id)

        return {
            "user_id": user_id,
            "restricted": False,
        }, 200
