from sqlalchemy import or_

from app.models.user import User
from app.storage.service import get_file_url

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
            "avatar": (get_file_url(u.profile_picture)if u.profile_picture
                       else None),    
        }
        for u in users
    ]