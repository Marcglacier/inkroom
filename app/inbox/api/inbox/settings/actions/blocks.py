# app/inbox/api/inbox/settings/actions/blocks.py

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.user import User
from app.models.settings.user_block import UserBlock
from app.inbox.services.settings.blocks.block_service import (
    BlockService,
)


class BlocksAPI(MethodView):
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
            return {"error": "Invalid block target"}, 400

        if not self._target_exists(current_id, user_id):
            return {"error": "User not found"}, 404

        blocked = UserBlock.query.filter_by(
            blocker_id=current_id,
            blocked_id=user_id,
        ).first() is not None

        return {
            "user_id": user_id,
            "blocked": blocked,
        }, 200

    @jwt_required()
    def post(self, user_id):
        current_id = int(get_jwt_identity())

        if current_id == user_id:
            return {"error": "You cannot block yourself"}, 400

        if not self._target_exists(current_id, user_id):
            return {"error": "User not found"}, 404

        created = BlockService.block(current_id, user_id)

        return {
            "user_id": user_id,
            "blocked": True,
        }, 201 if created else 200

    @jwt_required()
    def delete(self, user_id):
        current_id = int(get_jwt_identity())

        if current_id == user_id:
            return {"error": "Invalid block target"}, 400

        if not self._target_exists(current_id, user_id):
            return {"error": "User not found"}, 404

        BlockService.unblock(current_id, user_id)

        return {
            "user_id": user_id,
            "blocked": False,
        }, 200
