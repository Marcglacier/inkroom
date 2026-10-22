# app/users/profile/services/get_profile.py

from app.users.profile.services.get_profile_base import get_profile_base
from app.users.social.services.relationship_service import get_relationship
from app.users.social.services.follow_counts import get_follow_counts
from app.models.profile import Profile
from app.models.user import User
from app.models.settings.user_block import UserBlock


def get_profile(viewer_id, user_id):
    is_self = viewer_id == user_id

    # Check block direction before loading the real profile.
    if not is_self:
        block = UserBlock.query.filter(
            (
                (UserBlock.blocker_id == user_id)
                & (UserBlock.blocked_id == viewer_id)
            )
            | (
                (UserBlock.blocker_id == viewer_id)
                & (UserBlock.blocked_id == user_id)
            )
        ).first()

        if block and block.blocker_id == user_id:
            return {
                "id": user_id,
                "username": "deleted_user",
                "name": "Deleted User",
                "bio": None,
                "avatar_url": None,
                "cover_url": None,
                "location": None,
                "birthday": None,
                "social_links": [],
                "is_private": True,
                "joined_at": None,
                "followers_count": 0,
                "following_count": 0,
                "relationship": "blocked",
                "is_following": False,
                "is_followed_by": False,
                "can_message": False,
                "is_blocked": True,
                "is_blocker": False,
            }

    data = get_profile_base(user_id)
    profile = Profile.query.filter_by(user_id=user_id).first()

    counts = get_follow_counts(user_id)
    relationship = get_relationship(viewer_id, user_id)

    viewer_follows = relationship["following"]

    data.update({
        **counts,
        "relationship": relationship["state"],
        "is_following": relationship["following"],
        "is_followed_by": relationship["followed_by"],
        "can_message": (
            not relationship.get("blocked", False)
            and relationship["following"]
        ),
        "is_blocked": False,
        "is_blocker": (
            not is_self
            and UserBlock.query.filter_by(
                blocker_id=viewer_id,
                blocked_id=user_id,
            ).first() is not None
        ),
    })

    # Preserve existing private-profile behavior.
    if not is_self and profile.is_private and not viewer_follows:
        data["bio"] = None
        data["social_links"] = []

    return data
