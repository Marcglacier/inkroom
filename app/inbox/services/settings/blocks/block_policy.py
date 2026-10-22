# app/inbox/services/settings/block_policy.py

from sqlalchemy import or_

from app.models.settings.user_block import UserBlock


class BlockPolicy:
    @staticmethod
    def blocks_either_user(user_a_id, user_b_id):
        if user_a_id == user_b_id:
            return False

        return UserBlock.query.filter(
            or_(
                (
                    UserBlock.blocker_id == user_a_id
                ) & (
                    UserBlock.blocked_id == user_b_id
                ),
                (
                    UserBlock.blocker_id == user_b_id
                ) & (
                    UserBlock.blocked_id == user_a_id
                ),
            )
        ).first() is not None
