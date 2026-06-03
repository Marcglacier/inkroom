# app/users/views/follow_requests.py

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

from app.models.follow_request import FollowRequest
from app.models.user import User


class FollowRequestsAPI(MethodView):

    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())

        requests = FollowRequest.query.filter_by(
            target_id=user_id
        ).all()

        # collect all requester IDs first (avoid N+1 queries)
        requester_ids = [r.requester_id for r in requests]

        users = User.query.filter(User.id.in_(requester_ids)).all()
        user_map = {u.id: u.username for u in users}

        return jsonify([
            {
                "user_id": r.requester_id,
                "username": user_map.get(r.requester_id, "unknown"),
                "status": "requested"
            }
            for r in requests
        ])