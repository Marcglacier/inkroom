# app/__init__.py
from flask import Flask

from .config import Config
from .extensions import db, migrate, jwt, socketio, oauth

from .auth.routes import auth_bp
from .blog.routes import blog_bp
from .comments.routes import comment_bp
from app.users import users_bp

from app.inbox.routes import create_inbox_blueprint
from app.inbox.sockets import register_socket_events

import app.realtime
from .models import *


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app)
    oauth.init_app(app)

    # Register socket events
    register_socket_events(socketio)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(comment_bp, url_prefix="/api")
    app.register_blueprint(users_bp, url_prefix="/api/users")

    inbox_bp = create_inbox_blueprint()
    app.register_blueprint(inbox_bp, url_prefix="/api/inbox")

    return app