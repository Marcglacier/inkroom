from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def debug_jwt(tag=""):
    try:
        verify_jwt_in_request()
        print(f"✅ JWT OK {tag}")
        print("USER ID:", get_jwt_identity())
    except Exception as e:
        print(f"❌ JWT FAILED {tag}")
        print(str(e))