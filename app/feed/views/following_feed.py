# app/feed/views/following_feed.py
from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.follow import Follow
from app.models.post import Post
from app.models.repost import Repost


class FollowingFeedAPI(MethodView):

    @jwt_required()
    def get(self):

        user_id = int(get_jwt_identity())

        # =====================================
        # STEP 1: GET FOLLOWING IDS
        # =====================================

        following_ids = [
            f.following_id
            for f in Follow.query.filter_by(follower_id=user_id)
        ]

        # include myself
        following_ids.append(user_id)

        # =====================================
        # STEP 2: FETCH POSTS
        # =====================================

        posts = Post.query.filter(
            Post.author_id.in_(following_ids)
        ).all()

        # =====================================
        # STEP 3: FETCH REPOSTS
        # =====================================

        reposts = Repost.query.filter(
            Repost.user_id.in_(following_ids)
        ).all()

        # =====================================
        # STEP 4: BUILD FEED EVENTS
        # =====================================

        feed_events = []

        # -------------------------------------
        # ORIGINAL POSTS
        # -------------------------------------

        for post in posts:

            feed_events.append({
                "feed_type": "post",

                "created_at": post.created_at,

                "post": {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,

                    "author": {
                        "id": post.author.id,
                        "username": post.author.username
                    },

                    "likes_count": post.likes_count,
                    "comments_count": post.comments_count,
                    "reposts_count": post.reposts_count
                }
            })

        # -------------------------------------
        # REPOST EVENTS
        # -------------------------------------

        for repost in reposts:

            post = repost.post

            feed_events.append({
                "feed_type": "repost",

                "created_at": repost.created_at,

                "reposted_by": {
                    "id": repost.user.id,
                    "username": repost.user.username
                },

                "post": {
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,

                    "author": {
                        "id": post.author.id,
                        "username": post.author.username
                    },

                    "likes_count": post.likes_count,
                    "comments_count": post.comments_count,
                    "reposts_count": post.reposts_count
                }
            })

        # =====================================
        # STEP 5: SORT FEED
        # =====================================

        feed_events.sort(
            key=lambda x: x["created_at"],
            reverse=True
        )

        # =====================================
        # STEP 6: RETURN RESPONSE
        # =====================================

        return jsonify({
            "feed": feed_events
        })