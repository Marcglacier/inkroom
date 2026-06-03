# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from authlib.integrations.flask_client import OAuth
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

socketio = SocketIO(cors_allowed_origins="*")
oauth = OAuth()
mail = Mail()


# =========================
# JWT DEBUG
# =========================

@jwt.invalid_token_loader
def invalid_token(reason):
    print("❌ INVALID TOKEN:", reason)
    return {"message": reason}, 422


@jwt.unauthorized_loader
def missing_token(reason):
    print("❌ MISSING TOKEN:", reason)
    return {"message": reason}, 401


@jwt.expired_token_loader
def expired_token(jwt_header, jwt_payload):
    print("❌ TOKEN EXPIRED")
    return {"message": "Token expired"}, 401