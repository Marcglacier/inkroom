from app.models.follow import Follow
from app.models.follow_request import FollowRequest
from app.extensions import db


def convert_requests_to_follow(user_id):

    pending_requests = FollowRequest.query.filter_by(
        target_id=user_id
    ).all()

    for req in pending_requests:

        exists = Follow.query.filter_by(
            follower_id=req.requester_id,
            following_id=user_id
        ).first()

        if not exists:
            db.session.add(
                Follow(
                    follower_id=req.requester_id,
                    following_id=user_id,
                    status="following"
                )
            )

        req.status = "accepted"

    db.session.commit()