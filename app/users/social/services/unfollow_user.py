# app/users/social/services/unfollow_user.py

from app.extensions import db
from app.models.follow import Follow


class UnfollowUserService:
    """
    Handles removal of a direct follow relationship.

    This service is responsible only for the database mutation.
    Relationship state is read through RelationshipService.
    Notifications and socket events are handled by higher layers.
    """

    def __init__(self, user_id: int, target_id: int):
        self.user_id = user_id
        self.target_id = target_id

    def execute(self) -> str:

        if self.user_id == self.target_id:
            return "cannot_unfollow_self"

        follow = (
            Follow.query
            .filter_by(
                follower_id=self.user_id,
                following_id=self.target_id,
            )
            .first()
        )

        if not follow:
            return "not_following"

        db.session.delete(follow)
        db.session.commit()

        return "unfollowed"
