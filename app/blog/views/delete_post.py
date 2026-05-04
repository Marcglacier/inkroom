# app/blog/views/delete_post.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.post import Post


class DeletePostAPI(MethodView):

    @jwt_required()
    def delete(self, post_id):

        post = Post.query.get_or_404(post_id)

        if post.author_id != int(get_jwt_identity()):
            return jsonify({"error": "Not authorized"}), 403

        db.session.delete(post)
        db.session.commit()

        return jsonify({"message": "Post deleted"})