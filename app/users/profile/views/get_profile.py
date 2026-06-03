# app/users/profile/views/get_profile.py

from flask.views import MethodView
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.users.profile.services.get_profile import get_profile


class GetProfileAPI(MethodView):

    @jwt_required()
    def get(self, user_id):

        print("\n============================")
        print("🔥 GetProfileAPI HIT")
        print("============================")

        # ✅ AUTH USER
        viewer_id = int(get_jwt_identity())

        print("👤 VIEWER ID:", viewer_id)
        print("🎯 TARGET USER ID:", user_id)

        # ✅ FETCH PROFILE
        profile_data = get_profile(viewer_id, user_id)

        print("\n📦 PROFILE RESPONSE:")
        print(profile_data)

        # ✅ IMPORTANT DEBUGS
        print("\n🧠 DEBUG VALUES")
        print("📅 JOINED AT:", profile_data.get("joined_at"))
        print("🔗 SOCIAL LINKS:", profile_data.get("social_links"))
        print("📝 BIO:", profile_data.get("bio"))
        print("🔒 IS PRIVATE:", profile_data.get("is_private"))

        # detect empty values
        if not profile_data.get("social_links"):
            print("⚠️ NO SOCIAL LINKS RETURNED")

        if profile_data.get("social_links") == {}:
            print("⚠️ SOCIAL LINKS IS EMPTY OBJECT")

        if profile_data.get("social_links") == []:
            print("⚠️ SOCIAL LINKS IS EMPTY ARRAY")

        print("============================\n")

        return jsonify(profile_data)