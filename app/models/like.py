# like.py
from app.extensions import db


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))