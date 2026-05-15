# app/users/services/accept_follow.py

from app.extensions import db

from app.models.follow import Follow
from app.models.follow_request import FollowRequest

from app.users.services.helpers import response

from app.notifications.services import (
    create_follow_accept_notification
)


def accept_follow(user_id, requester_id):

    request = FollowRequest.query.filter_by(
        requester_id=requester_id,
        target_id=user_id
    ).first()

    if not request:
        return {"error": "Request not found"}, 404

    # =========================
    # CREATE OR UPDATE FOLLOW
    # =========================
    follow = Follow.query.filter_by(
        follower_id=requester_id,
        following_id=user_id
    ).first()

    if not follow:
        follow = Follow(
            follower_id=requester_id,
            following_id=user_id,
            status="following"
        )
        db.session.add(follow)

    else:
        follow.status = "following"

    # =========================
    # REMOVE REQUEST
    # =========================
    db.session.delete(request)

    db.session.commit()

    # =========================
    # NOTIFICATION (IMPORTANT FIX)
    # =========================
    create_follow_accept_notification(
        actor_id=user_id,
        target_user_id=requester_id
    )

    return response(
        "Follow request accepted",
        "following",
        follower_id=requester_id,
        following_id=user_id
    )