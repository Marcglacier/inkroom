# app/users/services/reject_follow.py
from app.extensions import db

from app.models.follow_request import FollowRequest

from app.users.services.helpers import response


def reject_follow(user_id, requester_id):

    request = FollowRequest.query.filter_by(
        requester_id=requester_id,
        target_id=user_id
    ).first()

    if not request:
        return {
            "error": "Request not found"
        }, 404

    db.session.delete(request)

    db.session.commit()

    return response(
        "Follow request rejected",
        "rejected",
        follower_id=requester_id,
        following_id=user_id
    )