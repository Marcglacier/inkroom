# app/auth/resolvers/user_resolver.py
from app.models.user import User


class UserResolver:

    @staticmethod
    def by_email(email: str):
        return (
            User.query
            .filter_by(email=email)
            .first()
        )

    @staticmethod
    def by_username(username: str):
        return (
            User.query
            .filter_by(username=username)
            .first()
        )