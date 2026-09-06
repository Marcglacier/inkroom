# app/users/profile/views/upload_cover.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.users.profile.services.upload_cover import upload_cover


class UploadCoverAPI(MethodView):

    @jwt_required()
    def post(self):

        user_id = int(get_jwt_identity())

        file = request.files.get("file")

        if not file:
            return jsonify({
                "error": "No cover image provided"
            }), 400

        result = upload_cover(
            user_id=user_id,
            file=file,
        )

        return jsonify(result), 200