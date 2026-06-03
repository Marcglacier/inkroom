from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user import User
from app.users.profile.services.get_profile import get_profile


class GetUserByUsernameAPI(MethodView):

    @jwt_required()
    def get(self, username):

        print("\n============================")
        print("🔥 GetUserByUsernameAPI HIT")
        print("🔥 USERNAME:", username)

        # AUTH USER
        viewer_id = int(get_jwt_identity())
        print("🔥 VIEWER ID:", viewer_id)

        # TARGET USER
        user = User.query.filter_by(username=username).first()

        if not user:
            print("❌ USER NOT FOUND")
            return {
                "message": "User not found"
            }, 404

        print("✅ TARGET USER:", user.username)
        print("✅ TARGET USER ID:", user.id)

        # USE MAIN PROFILE SERVICE
        profile_data = get_profile(viewer_id, user.id)

        print("📦 FINAL PROFILE RESPONSE:")
        print(profile_data)

        print("============================\n")

        return profile_data