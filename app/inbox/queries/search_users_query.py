from sqlalchemy import or_

from app.models.user import User


def search_inbox_users(user_id, text):

    if not text or not text.strip():
        return []

    text = text.strip()

    users = (
        User.query
        .filter(
            User.id != user_id,
            or_(
                User.username.ilike(f"%{text}%"),
                User.name.ilike(f"%{text}%")
            )
        )
        .limit(20)
        .all()
    )


    return [
        {
            "user_id": u.id,
            "username": u.username,
            "name": u.name,
            "avatar":
                u.profile.avatar_url
                if u.profile
                else None
        }
        for u in users
    ]