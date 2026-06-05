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

    result = {
        "state": _compute_state(following, followed_back, request),
        "is_mutual": following and followed_back,
        "following": following,
        "followed_back": followed_back,
        "requested": request is not None
    }


    return result

def _compute_state(following, followed_back, request):

    if following and followed_back:
        return "mutual"

    if following:
        return "following"

    if request:
        return "requested"

    return "none"