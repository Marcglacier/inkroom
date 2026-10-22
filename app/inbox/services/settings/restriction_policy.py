# app/inbox/services/settings/restriction_policy.py
from sqlalchemy import or_

from app.models.settings.user_restriction import UserRestriction


class RestrictionPolicy:
    @staticmethod
    def restricts_either_user(user_a_id, user_b_id):
        if user_a_id == user_b_id:
            return False

        return UserRestriction.query.filter(
            or_(
                (
                    UserRestriction.restricter_id == user_a_id
                ) & (
                    UserRestriction.restricted_id == user_b_id
                ),
                (
                    UserRestriction.restricter_id == user_b_id
                ) & (
                    UserRestriction.restricted_id == user_a_id
                ),
            )
        ).first() is not None