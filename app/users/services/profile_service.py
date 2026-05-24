from app.models.user import User
from app.models.profile import Profile
from app.models.follow import Follow
from app.extensions import db
from datetime import datetime

def get_profile(viewer_id, user_id):
    user = User.query.get_or_404(user_id)

    profile = Profile.query.filter_by(user_id=user_id).first()
    if not profile:
        profile = Profile(user_id=user_id)
        db.session.add(profile)
        db.session.commit()

    is_self = viewer_id == user_id

    # =========================
    # FOLLOW DATA (ONLY ACCEPTED)
    # =========================
    followers_count = Follow.query.filter_by(
        following_id=user_id,
        status="accepted"
    ).count()

    following_count = Follow.query.filter_by(
        follower_id=user_id,
        status="accepted"
    ).count()

    viewer_follows = Follow.query.filter_by(
        follower_id=viewer_id,
        following_id=user_id,
        status="accepted"
    ).first() is not None

    target_follows = Follow.query.filter_by(
        follower_id=user_id,
        following_id=viewer_id,
        status="accepted"
    ).first() is not None

    relationship = (
        "self" if is_self else
        "mutual" if viewer_follows and target_follows else
        "following" if viewer_follows else
        "followed_by" if target_follows else
        "none"
    )

    is_requested = Follow.query.filter_by(
        follower_id=viewer_id,
        following_id=user_id,
        status="requested"
    ).first() is not None

    # =========================
    # JOINED AT (MONTH + YEAR ONLY)
    # =========================
    joined_at = None
    if user.created_at:
          joined_at = user.created_at.strftime("%B %Y")   # e.g. "May 2026"
    print("JOINED_AT DEBUG:", joined_at)
    # =========================
    # RESPONSE
    # =========================
    data = {
        "id": user.id,
        "username": user.username,
        "name": user.name,

        "bio": profile.bio,
        "avatar_url": profile.avatar_url,

        "followers_count": followers_count,
        "following_count": following_count,

        "is_private": profile.is_private,

        "relationship": relationship,
        "is_following": viewer_follows,
        "is_followed_by": target_follows,
        "is_requested": is_requested,

        "can_message": viewer_follows and target_follows,

        # 👇 ALWAYS allow self view
        "location": profile.location if is_self else None,
        "birthday": profile.birthday.isoformat() if (is_self and profile.birthday) else None,
        "joined_at": joined_at,
    }

    # =========================
    # PRIVACY RULES
    # =========================
    if profile.is_private and not is_self and not viewer_follows:
        data["social_links"] = {}
        data["bio"] = None
    else:
        data["social_links"] = profile.social_links or {}

    return data


# =========================
# UPDATE PROFILE
# =========================
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

    if "social_links" in data:
        profile.social_links = data["social_links"]

    user = User.query.get(user_id)
    if "name" in data:
        user.name = data["name"]

    db.session.commit()

    return {"message": "Profile updated"}