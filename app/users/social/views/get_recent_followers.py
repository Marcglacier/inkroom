from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.users.social.services.get_recent_followers import ( get_recent_followers)


class RecentFollowersView(MethodView):

    decorators = [jwt_required()]

    def get(self):
        print("RECENT FOLLOWERS QUERY HIT")

        user_id = int(get_jwt_identity())
        results = get_recent_followers(user_id)

        print("RESULT:", results)

        return {"followers": results}, 200