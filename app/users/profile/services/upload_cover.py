# app/users/profile/services/upload_cover.py

from app.extensions import db
from app.models.profile import Profile
from app.storage.folders import cover_folder
from app.storage.service import upload_file


class UploadCoverService:
    """
    Handles profile cover uploads.

    This service owns the file upload and profile mutation.
    """

    def __init__(self, user_id: int, file):
        self.user_id = user_id
        self.file = file

    def execute(self) -> dict:
        profile = self._get_profile()

        result = self._upload_cover()

        profile.cover_url = result["object_key"]

        db.session.commit()

        return {
            "cover_url": profile.cover_url,
        }

    # =========================
    # PROFILE
    # =========================

    def _get_profile(self) -> Profile:
        profile = (
            Profile.query
            .filter_by(user_id=self.user_id)
            .first()
        )

        if not profile:
            raise RuntimeError("Profile not found")

        return profile

    # =========================
    # STORAGE
    # =========================

    def _upload_cover(self) -> dict:
        return upload_file(
            file=self.file,
            folder=cover_folder(self.user_id),
        )


def upload_cover(user_id: int, file) -> dict:
    return UploadCoverService(
        user_id=user_id,
        file=file,
    ).execute()