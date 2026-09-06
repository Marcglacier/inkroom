# app/users/profile/services/get_profile_base.py
from app.models.user import User
from app.models.profile import Profile
from app.extensions import db
from app.users.profile.services.helpers import (
    format_joined_at,
    safe_iso,
)
from app.storage.service import get_file_url


class GetProfileBaseService:
    """
    Builds the base profile representation.

    This service owns:
    - User lookup
    - Profile lookup/creation
    - Avatar URL generation
    - Cover URL generation
    - Base profile serialization
    """

    def __init__(self, user_id: int):
        self.user_id = user_id
        self.user = None
        self.profile = None

    def execute(self) -> dict:
        self._load_user()
        self._load_profile()

        return self._build_profile()

    # =========================
    # USER
    # =========================

    def _load_user(self) -> None:
        self.user = User.query.get_or_404(self.user_id)

    # =========================
    # PROFILE
    # =========================

    def _load_profile(self) -> None:
        self.profile = (
            Profile.query
            .filter_by(user_id=self.user_id)
            .first()
        )

        if not self.profile:
            self.profile = Profile(
                user_id=self.user_id
            )

            db.session.add(self.profile)
            db.session.commit()

    # =========================
    # STORAGE
    # =========================

    def _get_avatar_url(self) -> str | None:
        if not self.user.profile_picture:
            return None

        return get_file_url(
            self.user.profile_picture
        )

    def _get_cover_url(self) -> str | None:
        if not self.profile.cover_url:
            return None

        return get_file_url(
            self.profile.cover_url
        )

    # =========================
    # SERIALIZATION
    # =========================

    def _build_profile(self) -> dict:
        return {
            "id": self.user.id,
            "username": self.user.username,
            "name": self.user.name,

            "bio": self.profile.bio,

            "avatar_url": self._get_avatar_url(),
            "cover_url": self._get_cover_url(),

            "location": self.profile.location,
            "birthday": safe_iso(
                self.profile.birthday
            ),

            "social_links": (
                self.profile.social_links or []
            ),

            "is_private": self.profile.is_private,

            "joined_at": format_joined_at(
                self.user
            ),
        }


def get_profile_base(user_id: int) -> dict:
    return GetProfileBaseService(
        user_id=user_id
    ).execute()