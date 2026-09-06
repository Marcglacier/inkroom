# app/users/social/services/follow_counts.py
from app.models.follow import Follow


class FollowCountService:
    """
    Single source of truth for follower/following counts.

    Counts are always derived from the Follow table.
    """

    def __init__(self, user_id: int):
        self.user_id = user_id

    def get(self) -> dict:
        return {
            "followers_count": self._followers_count(),
            "following_count": self._following_count(),
        }

    def _followers_count(self) -> int:
        return (
            Follow.query
            .filter_by(
                following_id=self.user_id,
            )
            .count()
        )

    def _following_count(self) -> int:
        return (
            Follow.query
            .filter_by(
                follower_id=self.user_id,
            )
            .count()
        )


def get_follow_counts(user_id: int) -> dict:
    """
    Compatibility wrapper for existing callers.
    """

    return FollowCountService(user_id).get()