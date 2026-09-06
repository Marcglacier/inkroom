# __init__.py
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
from app.sockets import register_socket_events
from flask import g, request, make_response
from app.infrastructure import (
    configure_logging, generate_request_id, set_request_id, get_request_id,
    clear_request_id, RequestLogger, ExceptionHandler, health_bp, monitoring_bp, start_monitoring,
)

def create_app():

    configure_logging()

    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), "static")
    )

    app.config.from_object(Config)
    ExceptionHandler.register(app)

    # CORS
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "http://localhost:5173"
            }
        },
        supports_credentials=True,
        allow_headers=[
            "Content-Type",
            "Authorization",
            "X-Request-ID",
        ],
        methods=[
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "OPTIONS",
        ],
    )

    # REQUEST ID
    @app.before_request
    def assign_request_id():

        request_id = request.headers.get(
            "X-Request-ID"
        )

        if not request_id:
            request_id = generate_request_id()

        set_request_id(request_id)

        g.request_id = request_id
        
    @app.before_request
    def start_request_logging():

        g.request_started_at = (
        RequestLogger.start()
    )    
        
    @app.after_request
    def log_request(response):

        RequestLogger.finish(
            g.request_started_at,
            response.status_code,
    )

        return response

    @app.after_request
    def attach_request_id(response):

        response.headers[
            "X-Request-ID"
        ] = get_request_id() or "-"

        return response

    @app.teardown_request
    def cleanup_request_context(exception=None):

        clear_request_id()

    # CORS PREFLIGHT
    @app.before_request
    def handle_preflight():

        if request.method == "OPTIONS":
            return make_response("", 200)

    # EXTENSIONS
    db.init_app(app)

    migrate.init_app(app, db)

    jwt.init_app(app)

    mail.init_app(app)

    socketio.init_app(
        app,
        cors_allowed_origins=app.config[
            "SOCKETIO_CORS_ORIGINS"
        ],
        message_queue=app.config[
            "SOCKETIO_MESSAGE_QUEUE"
        ],
    )
    oauth.init_app(app)

    # OAUTH
    oauth.register(
        name="google",
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    # SOCKET EVENTS (CENTRALIZED)
    register_socket_events(socketio)

    # BLUEPRINTS
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(blog_bp, url_prefix="/api/blog")
    app.register_blueprint(comment_bp, url_prefix="/api")
    app.register_blueprint(users_bp, url_prefix="/api/users")

    inbox_bp = create_inbox_blueprint()
    app.register_blueprint(inbox_bp, url_prefix="/api/inbox")

    app.register_blueprint(notifications_bp, url_prefix="/api/notifications")
    app.register_blueprint(feed_bp, url_prefix="/api/feed")
    app.register_blueprint(search_bp, url_prefix="/api/search")
    app.register_blueprint(health_bp, url_prefix="/api/")
    app.register_blueprint( monitoring_bp, url_prefix="/api/", )

    # MEDIA ROUTES
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

    # BACKGROUND MONITORING
    return app