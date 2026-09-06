# app/users/social/services/relationship_service.py

from app.models.follow import Follow
from app.models.follow_request import FollowRequest


class RelationshipService:
    """
    Read-only authority for the relationship between two users.

    This service does not mutate relationship data.

    It answers one question:

        "What is the current relationship between viewer and target?"

    All relationship state is derived from:
        - follows
        - follow requests
    """

    def __init__(self, viewer_id: int, target_id: int):
        self.viewer_id = viewer_id
        self.target_id = target_id

    def get(self) -> dict:
        following = self._is_following(
            self.viewer_id,
            self.target_id,
        )

        followed_by = self._is_following(
            self.target_id,
            self.viewer_id,
        )

        request_sent = self._request_exists(
            self.viewer_id,
            self.target_id,
        )

        request_received = self._request_exists(
            self.target_id,
            self.viewer_id,
        )

        return {
            "following": following,
            "followed_by": followed_by,
            "is_mutual": following and followed_by,
            "request_sent": request_sent,
            "request_received": request_received,
            "state": self._resolve_state(
                following=following,
                followed_by=followed_by,
                request_sent=request_sent,
                request_received=request_received,
            ),
        }

    # ---------------------------------------------------------
    # DATABASE FACTS
    # ---------------------------------------------------------

    @staticmethod
    def _is_following(
        follower_id: int,
        following_id: int,
    ) -> bool:

        return (
            Follow.query
            .filter_by(
                follower_id=follower_id,
                following_id=following_id,
            )
            .first()
            is not None
        )

    @staticmethod
    def _request_exists(
        requester_id: int,
        target_id: int,
    ) -> bool:

        return (
            FollowRequest.query
            .filter_by(
                requester_id=requester_id,
                target_id=target_id,
            )
            .first()
            is not None
        )

    # ---------------------------------------------------------
    # DERIVED STATE
    # ---------------------------------------------------------

    @staticmethod
    def _resolve_state(
        *,
        following: bool,
        followed_by: bool,
        request_sent: bool,
        request_received: bool,
    ) -> str:

        # Both users follow each other
        if following and followed_by:
            return "mutual"

        # Someone has requested to follow me.
        # This must come before "following" because I may
        # already follow them while their request is pending.
        if request_received:
            return "request_received"

        # I requested to follow someone with a private account.
        if request_sent:
            return "requested"

        # I follow them.
        if following:
            return "following"

        # They follow me, but I don't follow them.
        if followed_by:
            return "follower"

        return "none"


def get_relationship(viewer_id: int, target_id: int) -> dict:
    """
    Compatibility wrapper for existing callers.

    New code should prefer RelationshipService directly.
    """

    return RelationshipService(
        viewer_id,
        target_id,
    ).get()