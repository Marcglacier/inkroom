# app/users/social/services/relationship_service.py

from app.models.follow import Follow
from app.models.follow_request import FollowRequest


def get_relationship(viewer_id, target_id):

    follow = Follow.query.filter_by(
        follower_id=viewer_id,
        following_id=target_id,
        status="following"
    ).first()

    reverse_follow = Follow.query.filter_by(
        follower_id=target_id,
        following_id=viewer_id,
        status="following"
    ).first()

    sent_request = FollowRequest.query.filter_by(
        requester_id=viewer_id,
        target_id=target_id,
        status="pending"
    ).first()

    received_request = FollowRequest.query.filter_by(
        requester_id=target_id,
        target_id=viewer_id,
        status="pending"
    ).first()

    following = follow is not None
    followed_back = reverse_follow is not None

    has_sent_request = sent_request is not None
    has_received_request = received_request is not None

    state = _compute_state(
        following,
        followed_back,
        has_sent_request,
        has_received_request
    )

    return {
        "state": state,

        # follow graph
        "following": following,
        "followed_back": followed_back,
        "is_mutual": following and followed_back,

        # 🔥 REQUEST SYSTEM (THIS FIXES YOUR UI)
        "has_sent_request": has_sent_request,
        "has_received_request": has_received_request,

        # optional legacy support (keep for now)
        "requested": has_sent_request,

        # button action
        "action": _compute_action(
            following,
            has_sent_request,
            has_received_request
        )
    }


def _compute_state(
    following: bool,
    followed_back: bool,
    sent_request: bool,
    received_request: bool
):

    # 🔥 PRIORITY: REQUEST STATE FIRST
    if sent_request:
        return "raven_sent"

    if received_request:
        return "oath_received"

    # FOLLOW STATES
    if following and followed_back:
        return "break_oath"

    if following:
        return "break_oath"

    if not following and followed_back:
        return "bind_oath"

    return "swear_oath"


def _compute_action(
    following: bool,
    sent_request: bool,
    received_request: bool
):

    # follower logic
    if following:
        return "unfollow"

    if sent_request:
        return "cancel_request"

    if received_request:
        return "accept_or_reject"

    return "follow"