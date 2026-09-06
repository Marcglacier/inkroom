# app/users/social/services/convert_requests_to_follow.py
from app.extensions import db
from app.models.follow import Follow
from app.models.follow_request import FollowRequest


class ConvertRequestsToFollowService:
    """
    Converts all pending follow requests for a user
    into direct follow relationships.

    This is used when a private account becomes public.

    This service is responsible only for database mutation.

    It does not:
        - calculate relationship state
        - create notifications
        - emit socket events
        - commit the transaction
    """

    def __init__(self, user_id: int):
        self.user_id = user_id

    def execute(self) -> int:
        pending_requests = (
            FollowRequest.query
            .filter_by(target_id=self.user_id)
            .all()
        )

        converted = 0

        for request in pending_requests:

            existing_follow = (
                Follow.query
                .filter_by(
                    follower_id=request.requester_id,
                    following_id=self.user_id,
                )
                .first()
            )

            if not existing_follow:
                db.session.add(
                    Follow(
                        follower_id=request.requester_id,
                        following_id=self.user_id,
                    )
                )

                converted += 1

            db.session.delete(request)

        return converted