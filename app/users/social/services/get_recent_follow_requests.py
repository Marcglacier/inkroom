from datetime import datetime, timedelta

from app.models.follow_request import FollowRequest
from app.models.user import User
from app.models.profile import Profile


def get_recent_follow_requests(user_id, days=14):

    cutoff = datetime.utcnow() - timedelta(days=days)

    requests = (
        FollowRequest.query
        .filter(
            FollowRequest.target_id == user_id,
            FollowRequest.created_at >= cutoff
        )
        .order_by(FollowRequest.created_at.desc())
        .all()
    )

    result = []

    for req in requests:

        sender = User.query.get(req.requester_id)
        if not sender:
            continue

        profile = Profile.query.filter_by(user_id=sender.id).first()

        result.append({
            "id": req.id,
            "user_id": sender.id,
            "username": sender.username,
            "name": sender.name,
            "avatar": profile.avatar_url if profile else None,
            "created_at": req.created_at.isoformat(),
        })

    return result