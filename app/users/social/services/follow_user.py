# app/users/social/services/follow_user.py

from app.extensions import db
from app.models.follow import Follow
from app.models.follow_request import FollowRequest
from app.models.user import User
from app.models.profile import Profile
from app.users.social.services.relationship_service import RelationshipService


class FollowUserService:
    """
    Handles the act of following a user.

    This service is responsible for MUTATION only.

    It does not:
        - calculate relationship state
        - calculate follow counts
        - emit socket events
        - create notifications
        - build HTTP responses

    Relationship facts are read through RelationshipService.
    """

    def __init__(self, user_id: int, target_id: int):
        self.user_id = user_id
        self.target_id = target_id

    def execute(self) -> str:
        self._validate()

        relationship = RelationshipService(
            self.user_id,
            self.target_id,
        ).get()

        if relationship["following"]:
            return "already_following"

        if self._target_is_private():
            return self._send_request()

        return self._create_follow()

    # ======================= VALIDATION ============================

    def _validate(self):
        if self.user_id == self.target_id:
            raise ValueError("Cannot follow yourself")

        target = User.query.get(self.target_id)

        if target is None:
            raise LookupError("User not found")

    # ====================== PROFILE CHECK ==========================

    def _target_is_private(self) -> bool:
        profile = (
            Profile.query
            .filter_by(user_id=self.target_id)
            .first()
        )

        return profile.is_private if profile else False

    # ========================= MUTATIONS ===========================

    def _create_follow(self) -> str:
        follow = Follow(
            follower_id=self.user_id,
            following_id=self.target_id,
        )

        db.session.add(follow)
        db.session.commit()

        return "following"

    def _send_request(self) -> str:
        existing_request = (
            FollowRequest.query
            .filter_by(
                requester_id=self.user_id,
                target_id=self.target_id,
            )
            .first()
        )

        if existing_request:
            return "request_exists"

        request = FollowRequest(
            requester_id=self.user_id,
            target_id=self.target_id,
        )

        db.session.add(request)
        db.session.commit()

        return "requested"
