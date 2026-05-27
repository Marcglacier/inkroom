from app.models.follow import Follow
from app.models.follow_request import FollowRequest


def get_relationship(user_id, target_id):

    if user_id == target_id:
        return {
            "state": "self",
            "is_mutual": False,
            "following": False,
            "requested": False
        }

    # =========================
    # CHECK FOLLOW
    # =========================
    follow = Follow.query.filter_by(
        follower_id=user_id,
        following_id=target_id
    ).first()

    reverse_follow = Follow.query.filter_by(
        follower_id=target_id,
        following_id=user_id
    ).first()

    # =========================
    # CHECK REQUEST
    # =========================
    request = FollowRequest.query.filter_by(
        requester_id=user_id,
        target_id=target_id
    ).first()

    # =========================
    # BUILD STATE
    # =========================

    is_following = follow is not None and follow.status == "following"
    is_mutual = is_following and reverse_follow is not None

    if is_following:
        return {
            "state": "following",
            "is_mutual": is_mutual,
            "following": True,
            "requested": False
        }

    if request:
        return {
            "state": "requested",
            "is_mutual": False,
            "following": False,
            "requested": True
        }

    return {
        "state": "none",
        "is_mutual": False,
        "following": False,
        "requested": False
    }