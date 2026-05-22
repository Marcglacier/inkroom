from sqlalchemy import or_

from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment


def global_search(query):

    if not query:
        return {
            "users": [],
            "posts": [],
            "comments": []
        }

    like_query = f"%{query}%"

    # USERS
    users = User.query.filter(
        User.username.ilike(like_query)
    ).limit(10).all()

    # POSTS
    posts = Post.query.filter(
        or_(
            Post.title.ilike(like_query),
            Post.content.ilike(like_query)
        )
    ).limit(20).all()

    # COMMENTS + REPLIES
    comments = Comment.query.filter(
        Comment.content.ilike(like_query)
    ).limit(20).all()

    return {
  
        # USERS 
        "users": [
            {
                "id": user.id,
                "username": user.username
            }
            for user in users
        ],

        # POSTS
        "posts": [
            {
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
            for post in posts
        ],

        # COMMENTS
        "comments": [
            {
                "id": comment.id,
                "content": comment.content,

                "user": {
                    "id": comment.user.id,
                    "username": comment.user.username
                },

                "post": {
                    "id": comment.post.id,
                    "title": comment.post.title
                },

                # 🔥 tells frontend if reply
                "is_reply": comment.parent_id is not None,

                "parent_id": comment.parent_id
            }
            for comment in comments
        ]
    }