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

    request = FollowRequest.query.filter_by(
        requester_id=viewer_id,
        target_id=target_id
    ).first()

    following = follow is not None
    followed_back = reverse_follow is not None
    requested = request is not None

    state = _compute_state(
        following,
        followed_back,
        requested
    )

    return {
        "state": state,

        # frontend helpers
        "following": following,
        "followed_back": followed_back,
        "requested": requested,

        # mutual follow
        "is_mutual": following and followed_back,

        # button action
        "action": _compute_action(
            following,
            requested
        )
    }


def _compute_state(
    following: bool,
    followed_back: bool,
    requested: bool
):

    if following and followed_back:
        return "mutual"

    if following:
        return "following"

    if requested:
        return "requested"

    return "none"


def _compute_action(
    following: bool,
    requested: bool
):

    # clicking button should unfollow/cancel request
    if following:
        return "unfollow"

    if requested:
        return "cancel_request"

    return "follow"