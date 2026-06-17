from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.user import User
from app.users.profile.services.get_profile import get_profile


class GetUserByUsernameAPI(MethodView):

    @jwt_required()
    def get(self, username):

        print("\n============================")
        print("🔥 GetUserByUsernameAPI HIT")
        print("🔥 RAW USERNAME:", username)

        viewer_id = int(get_jwt_identity())
        print("🔥 VIEWER ID:", viewer_id)

        # normalize input
        raw = username.strip()
        safe = raw.lower()

        print("🧼 CLEAN INPUT:", safe)

        # 1️⃣ Try exact username match (FAST PATH)
        user = User.query.filter(
            User.username.ilike(raw)
        ).first()

        # 2️⃣ fallback: match by name (display name)
        if not user:
            print("⚠️ username not found, trying name fallback...")

            user = User.query.filter(
                User.name.ilike(raw)
            ).first()

        if not user:
            print("❌ USER NOT FOUND")
            print("🔎 SEARCHED VALUE:", raw)
            return {"message": "User not found"}, 404

        print("✅ FOUND USER:", user.username)
        print("✅ DISPLAY NAME:", user.name)
        print("✅ USER ID:", user.id)

        profile_data = get_profile(viewer_id, user.id)

        print("📦 FINAL PROFILE RESPONSE READY")
        print("============================\n")

        return profile_data