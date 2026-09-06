# app/auth/resolvers/pending_registration_resolver.py
from app.models.pending_registration import PendingRegistration


class PendingRegistrationResolver:

    @staticmethod
    def by_email(email: str):
        return (
            PendingRegistration.query
            .filter_by(email=email)
            .first()
        )

    @staticmethod
    def by_username(username: str):
        return (
            PendingRegistration.query
            .filter_by(username=username)
            .first()
        )