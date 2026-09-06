# app/users/profile/services/delete_account.py

from app.extensions import db
from app.models.user import User


class DeleteAccountService:

    def __init__(self, user_id):
        self.user_id = user_id

    def execute(self):
        user = db.session.get(User, self.user_id)

        if not user:
            return {
                "error": "Account no longer exists"
            }, 404

        try:
            user.is_deleted = True
            user.online = False
            
            db.session.commit()
            return {
                "message": "Account deleted successfully"
            }, 200

        except Exception:
            db.session.rollback()
            raise