from app.models.user import User
from app.models.profile import Profile
from app.extensions import db
from app.users.social.services.follow_request_service import convert_requests_to_follow


def update_profile(user_id, data):

    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile:
        profile = Profile(user_id=user_id)
        db.session.add(profile)

    old_private = profile.is_private

    profile.bio = data.get("bio", profile.bio)
    profile.location = data.get("location", profile.location)
    profile.social_links = data.get("social_links", profile.social_links)

    if "birthday" in data:
        profile.birthday = data["birthday"]

    if "is_private" in data:
        new_private = bool(data["is_private"])
        profile.is_private = new_private

        # SOCIAL DOMAIN HANDLED PROPERLY
        if old_private and not new_private:
            convert_requests_to_follow(user_id)

    user = User.query.get(user_id)

    if "name" in data:
        user.name = data["name"]

    db.session.commit()

    return {"message": "Profile updated"}