# app/users/services/profile_service.py
from app.models.user import User
from app.models.profile import Profile
from app.models.follow import Follow
from app.extensions import db


def get_profile(viewer_id, user_id):

    user = User.query.get_or_404(user_id)

    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile:
        profile = Profile(user_id=user_id)
        db.session.add(profile)
        db.session.commit()

    followers_count = Follow.query.filter_by(following_id=user_id).count()
    following_count = Follow.query.filter_by(follower_id=user_id).count()

    is_following = False

    if viewer_id != user_id:
        is_following = Follow.query.filter_by(
            follower_id=viewer_id,
            following_id=user_id
        ).first() is not None

    relationship = "self"

    if viewer_id != user_id:
        relationship = "following" if is_following else "not_following"

    profile_data = {
        "id": user.id,
        "username": user.username,
        "bio": profile.bio,
        "followers": followers_count,
        "following": following_count,
        "joined_at": user.created_at,
        "relationship": relationship,
        "is_private": profile.is_private
    }

    # Hide details if private and not following
    if profile.is_private and not is_following and viewer_id != user_id:
        profile_data.pop("bio")

    return profile_data


def update_profile(user_id, data):

    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile:
        profile = Profile(user_id=user_id)
        db.session.add(profile)

    profile.bio = data.get("bio", profile.bio)
    profile.location = data.get("location", profile.location)
    profile.avatar_url = data.get("avatar_url", profile.avatar_url)
    profile.is_private = data.get("is_private", profile.is_private)

    db.session.commit()

    return {"message": "Profile updated"}