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

socketio = SocketIO()

oauth = OAuth()
mail = Mail()