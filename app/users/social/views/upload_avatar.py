from flask.views import MethodView
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user import User
from app.users.profile.services.upload_avatar import upload_avatar

upload_bp = Blueprint("upload", __name__)


class UploadAvatarAPI(MethodView):
    @jwt_required()
    def post(self):
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        result = upload_avatar(user, file)

        return jsonify({
            "message": "Avatar uploaded successfully",
            **result,
        }), 200


upload_bp.add_url_rule(
    "/upload",
    view_func=UploadAvatarAPI.as_view("upload_avatar"),
    methods=["POST"],
)