# app/__init__.py
from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, socketio, oauth
from .auth.routes import auth_bp
from .blog.routes import blog_bp
from .comments.routes import comment_bp
from app.users import users_bp

from .models import *


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    socketio.init_app(app)
    oauth.init_app(app)


    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(comment_bp, url_prefix="/api")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    return app