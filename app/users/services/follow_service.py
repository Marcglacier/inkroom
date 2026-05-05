# app/services/follow_service.py
from app.extensions import db
from app.models.follow import Follow


class FollowService:

    @staticmethod
    def follow_user(follower_id, following_id):

        if follower_id == following_id:
            raise ValueError("You cannot follow yourself")

        existing = Follow.query.filter_by(
            follower_id=follower_id,
            following_id=following_id
        ).first()

        if existing:
            return False

        follow = Follow(
            follower_id=follower_id,
            following_id=following_id
        )

        db.session.add(follow)
        db.session.commit()

        return True


    @staticmethod
    def unfollow_user(follower_id, following_id):

        follow = Follow.query.filter_by(
            follower_id=follower_id,
            following_id=following_id
        ).first()

        if not follow:
            return False

        db.session.delete(follow)
        db.session.commit()

        return True


    @staticmethod
    def get_followers(user_id):

        return Follow.query.filter_by(
            following_id=user_id
        ).all()


    @staticmethod
    def get_following(user_id):

        return Follow.query.filter_by(
            follower_id=user_id
        ).all()