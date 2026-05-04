# app/auth/views/me.py
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify

from app.models.user import User


class MeAPI(MethodView):

    @jwt_required()
    def get(self):
        user_id = int(get_jwt_identity())

        user = User.query.get_or_404(user_id)

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })