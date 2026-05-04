# app/auth/views/register.py
from flask.views import MethodView
from flask import request, jsonify

from app.extensions import db
from app.models.user import User


class RegisterAPI(MethodView):

    def post(self):
        data = request.get_json()

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not all([username, email, password]):
            return jsonify({"error": "Missing fields"}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email exists"}), 400

        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return jsonify({"message": "User created"}), 201