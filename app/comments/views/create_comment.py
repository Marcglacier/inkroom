# app/comments/views/create_comment.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models import Comment


class CreateCommentAPI(MethodView):

    @jwt_required()
    def post(self):
        data = request.get_json()

        comment = Comment(
            content=data.get("content"),
            post_id=data.get("post_id"),
            parent_id=data.get("parent_id"),  # NULL = normal comment
            user_id=get_jwt_identity()
        )

        db.session.add(comment)
        db.session.commit()

        return jsonify({
            "message": "Comment created",
            "id": comment.id
        }), 201