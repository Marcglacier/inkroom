from app.models.user import User
from app.models.profile import Profile
from app.extensions import db
from app.users.profile.services.helpers import format_joined_at, safe_iso


def get_profile_base(user_id):

    user = User.query.get_or_404(user_id)

    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile:
        profile = Profile(user_id=user_id)
        db.session.add(profile)
        db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
        "name": user.name,
        "bio": profile.bio,
        "avatar_url": profile.avatar_url,
        "location": profile.location,
        "birthday": safe_iso(profile.birthday),
        "social_links": profile.social_links or [],
        "is_private": profile.is_private,
        "joined_at": format_joined_at(user),
    }