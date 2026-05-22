# app/users/services/profile_service.py
from app.models.user import User
from app.models.profile import Profile
from app.models.follow import Follow
from app.models.follow_request import FollowRequest
from app.extensions import db

def get_profile(viewer_id, user_id):

    user = User.query.get_or_404(user_id)

    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile:
        profile = Profile(user_id=user_id)
        db.session.add(profile)
        db.session.commit()

    followers_count = Follow.query.filter_by(
        following_id=user_id
    ).count()

    following_count = Follow.query.filter_by(
        follower_id=user_id
    ).count()

    viewer_follows = Follow.query.filter_by(
        follower_id=viewer_id,
        following_id=user_id
    ).first() is not None

    target_follows = Follow.query.filter_by(
        follower_id=user_id,
        following_id=viewer_id
    ).first() is not None

    is_self = viewer_id == user_id

    if is_self:
        relationship = "self"
    elif viewer_follows and target_follows:
        relationship = "mutual"
    elif viewer_follows:
        relationship = "following"
    elif target_follows:
        relationship = "followed_by"
    else:
        relationship = "none"

    is_requested = FollowRequest.query.filter_by(
        requester_id=viewer_id,
        target_id=user_id
    ).first() is not None

    data = {
        "id": user.id,
        "username": user.username,
        "bio": profile.bio,
        "followers": followers_count,
        "following": following_count,
        "is_private": profile.is_private,

        # 🔒 SELF ONLY
        "location": profile.location if is_self else None,
        "birthday": profile.birthday if is_self else None,
        "joined_at": user.created_at if is_self else None,

        "relationship": relationship,
        "is_following": viewer_follows,
        "is_followed_by": target_follows,
        "is_requested": is_requested,

        "can_message": viewer_follows and target_follows
    }

    if profile.is_private and not viewer_follows and not is_self:
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

    if "birthday" in data:
        profile.birthday = data["birthday"]

    if "is_private" in data:
        profile.is_private = bool(data["is_private"])

    db.session.commit()

    return {
        "message": "Profile updated",
        "is_private": profile.is_private
    }