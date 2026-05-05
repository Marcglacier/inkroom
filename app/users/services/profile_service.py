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

    # -------------------------
    # COUNTS (ONLY accepted follows)
    # -------------------------
    followers_count = Follow.query.filter_by(
        following_id=user_id,
        status="following"
    ).count()

    following_count = Follow.query.filter_by(
        follower_id=user_id,
        status="following"
    ).count()

    # -------------------------
    # RELATIONSHIP
    # -------------------------
    follow_rel = None

    if viewer_id != user_id:
        follow_rel = Follow.query.filter_by(
            follower_id=viewer_id,
            following_id=user_id
        ).first()

    if viewer_id == user_id:
        relationship = "self"
    elif not follow_rel:
        relationship = "none"
    else:
        relationship = follow_rel.status  # following | requested

    is_following = relationship == "following"
    is_requested = relationship == "requested"

    # -------------------------
    # BASE PROFILE
    # -------------------------
    data = {
        "id": user.id,
        "username": user.username,
        "bio": profile.bio,
        "location": profile.location,
        "followers": followers_count,
        "following": following_count,
        "joined_at": user.created_at,
        "is_private": profile.is_private,
        "relationship": relationship,
        "is_following": is_following,
        "is_requested": is_requested,
        "can_message": is_following
    }

    # -------------------------
    # PRIVACY RULES
    # -------------------------
    if profile.is_private and not is_following and viewer_id != user_id:
        data["bio"] = None
        data["visibility"] = "limited"

    return data


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