from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from authlib.integrations.flask_client import OAuth
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

socketio = SocketIO(
    cors_allowed_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    async_mode="threading",
    logger=True,
    engineio_logger=True
)

oauth = OAuth()
mail = Mail()