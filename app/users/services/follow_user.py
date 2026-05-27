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

DEBUG_FOLLOW = True


def log(msg):
    if DEBUG_FOLLOW:
        print(f"[FOLLOW DEBUG] {msg}")


def follow_user(user_id, target_id):

    log(f"START follow_user user_id={user_id}, target_id={target_id}")

    if user_id == target_id:
        return {"error": "Cannot follow yourself"}, 400

    user = User.query.get(target_id)

    if not user:
        return {"error": "User not found"}, 404

    profile = Profile.query.filter_by(user_id=target_id).first()
    is_private = profile.is_private if profile else False

    log(f"TARGET USER FOUND, is_private={is_private}")

    # =========================
    # CHECK EXISTING FOLLOW
    # =========================
    follow = Follow.query.filter_by(
        follower_id=user_id,
        following_id=target_id
    ).first()

    # =========================
    # IF ALREADY FOLLOWING → UNFOLLOW (TOGGLE)
    # =========================
    if follow:
        db.session.delete(follow)
        db.session.commit()

        log("❌ UNFOLLOWED USER")

        return response(
            "Unfollowed user",
            "none",
            follower_id=user_id,
            following_id=target_id
        )

    # =========================
    # PRIVATE ACCOUNT → REQUEST FLOW
    # =========================
    if is_private:

        log("🔒 PRIVATE FLOW ENTERED")

        req = FollowRequest.query.filter_by(
            requester_id=user_id,
            target_id=target_id
        ).first()

        # TOGGLE: cancel request if already exists
        if req:
            db.session.delete(req)
            db.session.commit()

            log("❌ FOLLOW REQUEST CANCELED")

            return response(
                "Follow request canceled",
                "none",
                follower_id=user_id,
                following_id=target_id
            )

        req = FollowRequest(
            requester_id=user_id,
            target_id=target_id
        )

        db.session.add(req)
        db.session.commit()

        create_follow_request_notification(
            actor_id=user_id,
            target_user_id=target_id
        )

        log("📩 FOLLOW REQUEST SENT")

        return response(
            "Follow request sent",
            "requested",
            follower_id=user_id,
            following_id=target_id
        )

    # =========================
    # PUBLIC ACCOUNT → DIRECT FOLLOW
    # =========================
    follow = Follow(
        follower_id=user_id,
        following_id=target_id,
        status="following"
    )

    db.session.add(follow)
    db.session.commit()

    create_follow_notification(
        actor_id=user_id,
        target_user_id=target_id
    )

    log("✅ FOLLOW CREATED")

    return response(
        "User followed",
        "following",
        follower_id=user_id,
        following_id=target_id
    )