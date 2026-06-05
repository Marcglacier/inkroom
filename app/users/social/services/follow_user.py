from app.extensions import db
from app.models.follow import Follow
from app.models.follow_request import FollowRequest
from app.models.user import User
from app.models.profile import Profile
from app.users.services.helpers import response
from app.notifications.services import (
    create_follow_notification,
    create_follow_request_notification
)

DEBUG = False

def log(*args):
    if DEBUG:
        print("[FOLLOW]", *args)


def follow_user(user_id, target_id):

    if user_id == target_id:
        return {"error": "Cannot follow yourself"}, 400

    user = User.query.get(target_id)
    if not user:
        return {"error": "User not found"}, 404

    is_private = (
        Profile.query.filter_by(user_id=target_id).first()
        or type("obj", (), {"is_private": False})()
    ).is_private

    follow = Follow.query.filter_by(
        follower_id=user_id,
        following_id=target_id
    ).first()

    # =========================
    # UNFOLLOW (TOGGLE OFF)
    # =========================
    if follow:
        db.session.delete(follow)
        db.session.commit()

        return response(
            "Unfollowed user",
            "none",
            follower_id=user_id,
            following_id=target_id
        )

    # =========================
    # PRIVATE → REQUEST FLOW
    # =========================
    if is_private:
        req = FollowRequest.query.filter_by(
            requester_id=user_id,
            target_id=target_id
        ).first()

        if req:
            db.session.delete(req)
            db.session.commit()

            return response(
                "Follow request canceled",
                "none",
                follower_id=user_id,
                following_id=target_id
            )

        db.session.add(FollowRequest(
            requester_id=user_id,
            target_id=target_id
        ))
        db.session.commit()

        create_follow_request_notification(
            actor_id=user_id,
            target_user_id=target_id
        )

        return response(
            "Follow request sent",
            "requested",
            follower_id=user_id,
            following_id=target_id
        )

    # =========================
    # PUBLIC → DIRECT FOLLOW
    # =========================
    db.session.add(Follow(
        follower_id=user_id,
        following_id=target_id,
        status="following"
    ))
    db.session.commit()

    create_follow_notification(
        actor_id=user_id,
        target_user_id=target_id
    )

    return response(
        "User followed",
        "following",
        follower_id=user_id,
        following_id=target_id
    )