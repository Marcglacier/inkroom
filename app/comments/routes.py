# app/comments/routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.comments.services import (
    create_comment_service,
    toggle_like_service,
    get_comments_service,
    delete_comment_service,
    update_comment_service
)

comment_bp = Blueprint("comments", __name__, url_prefix="/api")


@comment_bp.route("/comments", methods=["POST"])
@jwt_required()
def create_comment():
    data = request.get_json()
    user_id = get_jwt_identity()

    result, status = create_comment_service(data, user_id)
    return jsonify(result), status


@comment_bp.route("/comments/<int:comment_id>/like", methods=["POST"])
@jwt_required()
def like_comment(comment_id):
    user_id = get_jwt_identity()

    result, status = toggle_like_service(comment_id, user_id)
    return jsonify(result), status


@comment_bp.route("/posts/<int:post_id>/comments", methods=["GET"])
def get_comments(post_id):

    result = get_comments_service(post_id)
    return jsonify(result), 200


@comment_bp.route("/comments/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id):

    user_id = get_jwt_identity()

    result, status = delete_comment_service(comment_id, user_id)
    return jsonify(result), status


@comment_bp.route("/comments/<int:comment_id>", methods=["PUT"])
@jwt_required()
def update_comment(comment_id):

    data = request.get_json()
    user_id = get_jwt_identity()

    result, status = update_comment_service(comment_id, data, user_id)
    return jsonify(result), status