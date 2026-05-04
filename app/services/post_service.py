# app/services/post_service.py
from app.extensions import db
from app.models.post import Post


def create_post(author_id, title, content):

    if not title or not content:
        return None, "Missing fields"

    post = Post(
        title=title,
        content=content,
        author_id=author_id
    )

    db.session.add(post)
    db.session.commit()

    return post, None

def update_post(post_id, user_id, title=None, content=None):

    post = Post.query.get(post_id)

    if not post:
        return None, "Post not found", 404

    if post.author_id != user_id:
        return None, "Not authorized", 403

    if title is not None:
        post.title = title

    if content is not None:
        post.content = content

    db.session.commit()

    return post, None, None


def delete_post(post_id, user_id):

    post = Post.query.get(post_id)

    if not post:
        return None, "Post not found", 404

    if post.author_id != user_id:
        return None, "Not authorized", 403

    db.session.delete(post)
    db.session.commit()

    return True, None, None