from flask import Flask, send_from_directory
import os

from .config import Config
from .extensions import db, migrate, jwt, socketio, oauth, mail

from .auth.routes import auth_bp
from .blog.routes import blog_bp
from .comments.routes import comment_bp
from app.users import users_bp
from app.inbox.routes import create_inbox_blueprint

from app.notifications.routes import notifications_bp
from app.feed.routes import feed_bp
from app.search.routes import search_bp

from flask_cors import CORS

# ✅ ONLY IMPORT SOCKET REGISTRY (NOT INDIVIDUAL MODULES)
from app.sockets import register_socket_events


def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), "static")
    )

    app.config.from_object(Config)

    # =========================
    # CORS
    # =========================
    CORS(
        app,
        resources={r"/api/*": {"origins": "http://localhost:5173"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PATCH", "OPTIONS"]
    )

    # =========================
    # EXTENSIONS
    # =========================
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    socketio.init_app(
        app,
        cors_allowed_origins="*",
        async_mode="threading",
        logger=True,
        engineio_logger=True
    )

    oauth.init_app(app)

    # =========================
    # OAUTH
    # =========================
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    # =========================
    # SOCKET EVENTS (CENTRALIZED)
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
    # MEDIA ROUTES
    # =========================
    @app.route("/media/messages/<path:filename>")
    def serve_message_media(filename):
        return send_from_directory(
            os.path.join("storage", "messages"),
            filename
        )

    @app.route("/static/uploads/<path:filename>")
    def serve_upload(filename):
        upload_dir = os.path.join(app.static_folder, "uploads")
        return send_from_directory(upload_dir, filename)

    return app