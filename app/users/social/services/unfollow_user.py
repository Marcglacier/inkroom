from app.extensions import db
from app.models.follow import Follow
from app.models.follow_request import FollowRequest
from app.sockets.follow import emit_relationship_update


def unfollow_user(user_id, target_id):

    Follow.query.filter_by(
        follower_id=user_id,
        following_id=target_id
    ).delete(synchronize_session=False)

    FollowRequest.query.filter(
        (
            (FollowRequest.requester_id == user_id) &
            (FollowRequest.target_id == target_id)
        )
        |
        (
            (FollowRequest.requester_id == target_id) &
            (FollowRequest.target_id == user_id)
        )
    ).delete(synchronize_session=False)

    db.session.commit()

    emit_relationship_update(user_id, target_id)

    return {
        "message": "User unfollowed"
    }