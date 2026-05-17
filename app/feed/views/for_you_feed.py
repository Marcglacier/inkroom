# app/feed/views/for_you_feed.py
from flask.views import MethodView
from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app.models.post import Post
from app.models.repost import Repost
from app.feed.services.ranking import compute_post_score


class ForYouFeedAPI(MethodView):

    @jwt_required()
    def get(self):

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        # STEP 1: FETCH DATA

        posts = Post.query.all()
        reposts = Repost.query.all()

        feed_events = []

        # STEP 2: POSTS

        for post in posts:

            score = compute_post_score(post)

            feed_events.append({
                "feed_type": "post",
                "created_at": post.created_at,
                "score": score,

                "payload": {
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

        # STEP 3: REPOSTS

        for repost in reposts:

            post = repost.post

            # repost influence boost
            base_score = compute_post_score(post)
            repost_score = base_score + 3  # repost boost

            feed_events.append({
                "feed_type": "repost",
                "created_at": repost.created_at,
                "score": repost_score,

                "payload": {
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
                }
            })

        # STEP 4: SORT BY SCORE (NOT TIME)

        feed_events.sort(key=lambda x: x["score"], reverse=True)

        # STEP 5: PAGINATION (MANUAL)

        start = (page - 1) * per_page
        end = start + per_page

        paginated_feed = feed_events[start:end]

        return jsonify({
            "page": page,
            "per_page": per_page,
            "total": len(feed_events),
            "feed": paginated_feed
        })