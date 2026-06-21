from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Follow, User, Profile

class AlliesAPI(MethodView):
    @jwt_required()
    def get(self):
        uid = int(get_jwt_identity())
        ACTIVE = "following"

        sent_ids = {f.following_id for f in Follow.query.filter_by(follower_id=uid, status=ACTIVE).all()}
        received_ids = {f.follower_id for f in Follow.query.filter_by(following_id=uid, status=ACTIVE).all()}
        ally_ids = sent_ids & received_ids

        users = User.query.filter(User.id.in_(ally_ids)).all()
        allies = []
        for u in users:
            p = Profile.query.filter_by(user_id=u.id).first()
            allies.append({
                "id": u.id,
                "username": u.username,
                "name": u.name,
                "avatar": p.avatar_url if p else None
            })

        return {"allies": allies}, 200
