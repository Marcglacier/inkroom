# app/users/profile\services\update_profile.py
from app.extensions import db
from app.models.user import User
from app.models.profile import Profile
from app.users.social.services.convert_requests_to_follow import (
    ConvertRequestsToFollowService,
)
from app.users.profile.services.social_links.social_link_service import (
    SocialLinkService,
)


class UpdateProfileService:
    """
    Handles profile updates.

    This service owns the profile mutation and transaction.
    """

    def __init__(self, user_id: int, data: dict):
        self.user_id = user_id
        self.data = data

    def execute(self) -> dict:
        profile = self._get_or_create_profile()

        self._update_profile_fields(profile)
        self._handle_privacy_change(profile)

        user = self._get_user()
        self._update_user_fields(user)

        user.profile_completed = True

        db.session.commit()

        return {
            "message": "Profile updated"
        }

    # ======================= PROFILE ===========================

    def _get_or_create_profile(self) -> Profile:
        profile = (
            Profile.query
            .filter_by(user_id=self.user_id)
            .first()
        )

        if not profile:
            profile = Profile(user_id=self.user_id)
            db.session.add(profile)

        return profile

    def _update_profile_fields(self, profile: Profile) -> None:
        profile.bio = self.data.get(
            "bio",
            profile.bio,
        )

        profile.location = self.data.get(
            "location",
            profile.location,
        )

        if "social_links" in self.data:
            profile.social_links = SocialLinkService(
                self.data["social_links"]
            ).execute()

        if "birthday" in self.data:
            profile.birthday = self.data["birthday"]

    # ===================== PRIVACY ===============================

    def _handle_privacy_change(self, profile: Profile) -> None:
        if "is_private" not in self.data:
            return

        old_private = profile.is_private
        new_private = bool(self.data["is_private"])

        profile.is_private = new_private

        if old_private and not new_private:
            ConvertRequestsToFollowService(
                self.user_id
            ).execute()

    # ======================= USER ===============================

    def _get_user(self) -> User:
        return User.query.get(self.user_id)

    def _update_user_fields(self, user: User) -> None:
        if "name" in self.data:
            user.name = self.data["name"]

def update_profile(user_id: int, data: dict) -> dict:
    return UpdateProfileService(
        user_id,
        data,
    ).execute()