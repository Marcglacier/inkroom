from flask.views import MethodView
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = os.path.join(
    os.getcwd(),
    "app",
    "static",
    "uploads"
)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


class UploadAvatarAPI(MethodView):
    def post(self):
        print("Upload route hit:", request.files)

        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):

            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            file.save(filepath)

            print("ACTUAL FILEPATH:", filepath)

            url = f"{request.host_url}static/uploads/{filename}"

            return jsonify({
                "url": url
            }), 201

        return jsonify({"error": "Invalid file type"}), 400


upload_bp.add_url_rule(
    "/upload",
    view_func=UploadAvatarAPI.as_view("upload_avatar"),
    methods=["POST"],
)