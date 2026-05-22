from flask import Flask, send_from_directory
import os

from .config import Config
from .extensions import db, migrate, jwt, socketio, oauth

from .auth.routes import auth_bp
from .blog.routes import blog_bp
from .comments.routes import comment_bp
from app.users import users_bp

from app.inbox.routes import create_inbox_blueprint
from app.inbox.sockets import register_socket_events

from app.notifications.routes import notifications_bp
from app.feed.routes import feed_bp
from app.search.routes import search_bp

import app.realtime
from .models import *

from flask_cors import CORS
from .extensions import mail


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # =========================
    # CORS
    # =========================
    CORS(
        app,
        origins=["http://localhost:5173"],
        supports_credentials=True
    )

    # =========================
    # EXTENSIONS
    # =========================
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)
    socketio.init_app(app)
    oauth.init_app(app)

   # =========================
   # GOOGLE OAUTH (FIXED PROPERLY)
   # =========================
    oauth.register(
    name="google",
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
    )
    # =========================
    # SOCKET EVENTS
    # =========================
    register_socket_events(socketio)

    # =========================
    # BLUEPRINTS
    # =========================
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(blog_bp, url_prefix="/api/blog")
    app.register_blueprint(comment_bp, url_prefix="/api")
    app.register_blueprint(users_bp, url_prefix="/api/users")

    inbox_bp = create_inbox_blueprint()
    app.register_blueprint(inbox_bp, url_prefix="/api/inbox")

    app.register_blueprint(notifications_bp, url_prefix="/api/notifications")
    app.register_blueprint(feed_bp, url_prefix="/api/feed")
    app.register_blueprint(search_bp, url_prefix="/api/search")

    # =========================
    # MEDIA
    # =========================
    @app.route("/media/messages/<path:filename>")
    def serve_message_media(filename):
        return send_from_directory(
            os.path.join("storage", "messages"),
            filename
        )

    return app