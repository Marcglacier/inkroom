# app/blog/views/toggle_repost.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.repost import Repost
from app.models.post import Post
from app.notifications.services import create_notification

class ToggleRepostAPI(MethodView):

    @jwt_required()
    def post(self, post_id):

        user_id = int(get_jwt_identity())

        post = Post.query.get_or_404(post_id)

        existing = Repost.query.filter_by(
            user_id=user_id,
            post_id=post_id
        ).first()

        # =====================
        # UNDO REPOST
        # =====================
        if existing:
            db.session.delete(existing)

            # SAFE decrement (NO NEGATIVE VALUES)
            post.reposts_count = max(0, (post.reposts_count or 0) - 1)

            db.session.commit()

            return jsonify({
                "message": "Repost removed",
                "reposted": False
            }), 200

        # =====================
        # CREATE REPOST
        # =====================
        repost = Repost(
            user_id=user_id,
            post_id=post_id
        )

        db.session.add(repost)

        # SAFE increment
        post.reposts_count = (post.reposts_count or 0) + 1

        db.session.commit()
        
        # NOTIFY POST AUTHOR
        if user_id != post.author_id:
            create_notification(
                actor_id=user_id,
                user_id=post.author_id,
                type="REPOST",
                post_id=post.id
            )
            
        return jsonify({
            "message": "Post reposted",
            "reposted": True
        }), 201