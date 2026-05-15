# app/users/services/accept_follow.py
from app.extensions import db

from app.models.follow import Follow
from app.models.follow_request import FollowRequest
from app.users.services.helpers import response


def accept_follow(user_id, requester_id):

    request = FollowRequest.query.filter_by(
        requester_id=requester_id,
        target_id=user_id
    ).first()

    if not request:
        return {"error": "Request not found"}, 404

    # =========================
    # CHECK IF FOLLOW EXISTS
    # =========================
    follow = Follow.query.filter_by(
        follower_id=requester_id,
        following_id=user_id
    ).first()

    if not follow:
        follow = Follow(
            follower_id=requester_id,
            following_id=user_id,
            status="following"   # 🔥 IMPORTANT FIX
        )
        db.session.add(follow)

    else:
        follow.status = "following"

    # remove request
    db.session.delete(request)

    db.session.commit()

    return response(
        "Follow request accepted",
        "following",   # 🔥 FIXED (NOT accepted)
        follower_id=requester_id,
        following_id=user_id
    )