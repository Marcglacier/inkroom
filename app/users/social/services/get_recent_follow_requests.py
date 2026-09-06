from datetime import datetime, timedelta, timezone
from app.storage.service import get_file_url
from app.models.follow_request import FollowRequest
from app.models.user import User
from app.extensions import db

def get_recent_follow_requests(user_id, days=14):

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

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
        sender = db.session.get(User, req.requester_id)
        if not sender:
            continue


        created_at = req.created_at

        # 🔥 FORCE timezone-aware output
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        result.append({
            "id": req.id,
            "user_id": sender.id,
            "username": sender.username,
            "name": sender.name,
            "avatar": (get_file_url(sender.profile_picture) if sender.profile_picture else None),
            "created_at": created_at.isoformat()
        })

    return result