# app/users/social/services/reject_follow.py

from app.extensions import db
from app.models.follow_request import FollowRequest


class RejectFollowService:
    """
    Rejects a pending follow request.

    This service is responsible only for the relationship mutation.

    It does not:
        - calculate relationship state
        - create notifications
        - emit socket events
        - build HTTP responses
    """

    def __init__(self, user_id: int, requester_id: int):
        self.user_id = user_id
        self.requester_id = requester_id

    def execute(self) -> str:

        request = (
            FollowRequest.query
            .filter_by(
                requester_id=self.requester_id,
                target_id=self.user_id,
            )
            .first()
        )

        if not request:
            return "request_not_found"

        db.session.delete(request)
        db.session.commit()

        return "rejected"