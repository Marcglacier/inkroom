# app/comments/views/get_comments.py
from flask.views import MethodView
from flask import jsonify

from app.models import Comment


class GetCommentsAPI(MethodView):

    def get(self, post_id):

        comments = Comment.query.filter_by(
            post_id=post_id,
            parent_id=None
        ).all()

        def serialize(comment):
            return {
                "id": comment.id,
                "content": comment.content,
                "user_id": comment.user_id,
                "replies": [serialize(r) for r in comment.replies]
            }

        return jsonify([serialize(c) for c in comments])