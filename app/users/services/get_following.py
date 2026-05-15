# app/users/services/get_following.py
from app.models.follow import Follow


def get_following(user_id):

    return Follow.query.filter_by(
        follower_id=user_id
    ).all()