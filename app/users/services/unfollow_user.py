from app.extensions import db
from app.models.follow import Follow
from app.models.follow_request import FollowRequest
from app.users.services.helpers import response


def unfollow_user(user_id, target_id):

    # =========================
    # REMOVE FOLLOW RELATIONSHIP
    # =========================
    Follow.query.filter_by(
        follower_id=user_id,
        following_id=target_id
    ).delete(synchronize_session=False)

    # =========================
    # CLEAN UP FOLLOW REQUESTS (BOTH DIRECTIONS)
    # =========================
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

    # =========================
    # COMMIT ALL CHANGES
    # =========================
    db.session.commit()

    return response(
        "User unfollowed",
        "unfollowed",
        follower_id=user_id,
        following_id=target_id
    )