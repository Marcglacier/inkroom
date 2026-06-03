# app/users/profile/services/get_profile.py
from app.users.profile.services.get_profile_base import get_profile_base
from app.users.social.services.relationship_service import get_relationship
from app.users.social.services.follow_counts import get_follow_counts
from app.models.profile import Profile


def get_profile(viewer_id, user_id):

    data = get_profile_base(user_id)

    profile = Profile.query.filter_by(user_id=user_id).first()

    counts = get_follow_counts(user_id)

    relationship = get_relationship(viewer_id, user_id)

    viewer_follows = relationship["following"]
    target_follows = relationship["is_mutual"]

    is_self = viewer_id == user_id

    data.update({
      **counts,
      "relationship": relationship["state"],
      "is_following": relationship["following"],
      "is_followed_by": relationship["is_mutual"] or relationship["following"],
      "can_message": relationship["following"] and relationship["following"],
    })

    # privacy rules (kept here intentionally — policy layer)
    if not is_self and profile.is_private and not viewer_follows:
        data["bio"] = None
        data["social_links"] = []

    return data