# resolvers/__init__.py
from .user_resolver import UserResolver
from .pending_registration_resolver import PendingRegistrationResolver

__all__ = [
    "UserResolver",
    "PendingRegistrationResolver"
]