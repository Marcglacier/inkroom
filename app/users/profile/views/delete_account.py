# app/users/profile/views/delete_account.py

from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.users.profile.services.delete_account import DeleteAccountService


class DeleteAccountAPI(MethodView):

    @jwt_required()
    def delete(self):

        user_id = int(get_jwt_identity())

        service = DeleteAccountService(user_id)

        return service.execute()