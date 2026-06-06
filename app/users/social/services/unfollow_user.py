from app.extensions import db
from app.models.follow import Follow
from app.models.follow_request import FollowRequest
from app.users.services.helpers import response


def unfollow_user(user_id, target_id):

    deleted = Follow.query.filter_by(
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

    return {
        "message": "User unfollowed",
        "deleted": deleted
    }