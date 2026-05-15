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

    # FOLLOW COUNTS
    followers_count = Follow.query.filter_by(following_id=user_id).count()
    following_count = Follow.query.filter_by(follower_id=user_id).count()

    # RELATIONSHIP (viewer ↔ target)
    viewer_follows = Follow.query.filter_by(
        follower_id=viewer_id,
        following_id=user_id
    ).first() is not None

    target_follows = Follow.query.filter_by(
        follower_id=user_id,
        following_id=viewer_id
    ).first() is not None

    if viewer_id == user_id:
        relationship = "self"
    elif viewer_follows and target_follows:
        relationship = "mutual"
    elif viewer_follows:
        relationship = "following"
    elif target_follows:
        relationship = "followed_by"
    else:
        relationship = "none"

    is_following = viewer_follows
    is_followed_by = target_follows
    is_requested = FollowRequest.query.filter_by(
        requester_id=viewer_id,
        target_id=user_id
    ).first() is not None

    # RESPONSE
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
        "is_followed_by": is_followed_by,
        "is_requested": is_requested,

        "can_message": is_following and is_followed_by
    }

    # PRIVACY RULES
    if profile.is_private and not is_following and viewer_id != user_id:
        data["bio"] = None
        data["location"] = None
        data["visibility"] = "limited"

    return data

# PROFILE UPDATE (PRIVATE TOGGLE ENABLED)
def update_profile(user_id, data):

    profile = Profile.query.filter_by(user_id=user_id).first()

    if not profile:
        profile = Profile(user_id=user_id)
        db.session.add(profile)

    profile.bio = data.get("bio", profile.bio)
    profile.location = data.get("location", profile.location)
    profile.avatar_url = data.get("avatar_url", profile.avatar_url)

    if "is_private" in data:
        profile.is_private = bool(data["is_private"])

    db.session.commit()

    return {
        "message": "Profile updated",
        "is_private": profile.is_private
    }