# app/users/services/get_following.py
from app.models.follow import Follow


def get_followers(user_id):

    return Follow.query.filter_by(
        following_id=user_id
    ).all()