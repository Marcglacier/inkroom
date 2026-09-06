# app/inbox/api/inbox/get_allies.py
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import Follow, User
from app.storage.service import get_file_url


class AlliesAPI(MethodView):
    @jwt_required()
    def get(self):
        uid = int(get_jwt_identity())

        # People I follow
        sent_ids = {
            f.following_id
            for f in Follow.query.filter_by(
                follower_id=uid
            ).all()
        }

        # People who follow me
        received_ids = {
            f.follower_id
            for f in Follow.query.filter_by(
                following_id=uid
            ).all()
        }

        # Mutual follows = allies
        ally_ids = sent_ids & received_ids

        users = User.query.filter(
            User.id.in_(ally_ids)
        ).all()

        allies = []

        for u in users:
            allies.append({
                "id": u.id,
                "username": u.username,
                "name": u.name,
                "avatar": (
                    get_file_url(u.profile_picture)
                    if u.profile_picture
                    else None
                ),
            })

        return {"allies": allies}, 200