# app/infrastructure/logging/handlers/exception_handler.py

import logging

from flask import jsonify
from werkzeug.exceptions import HTTPException

from ..request_context import get_request_id

logger = logging.getLogger("inkroom.error")


class ExceptionHandler:

    @staticmethod
    def register(app):

        # =========================
        # HTTP ERRORS
        # =========================
        @app.errorhandler(HTTPException)
        def handle_http_exception(error):

            request_id = (
                get_request_id()
                or "-"
            )

            logger.warning(
                "HTTP error | "
                "request_id=%s | "
                "status=%s | "
                "error=%s",
                request_id,
                error.code,
                error,
            )

            return jsonify({
                "error": (
                    error.name
                    .lower()
                    .replace(" ", "_")
                ),
                "message": error.description,
                "request_id": request_id,
            }), error.code

        # =========================
        # UNEXPECTED APPLICATION ERRORS
        # =========================
        @app.errorhandler(Exception)
        def handle_exception(error):

            request_id = (
                get_request_id()
                or "-"
            )

            logger.exception(
                "Unhandled exception | "
                "request_id=%s | "
                "error=%s",
                request_id,
                error,
            )

            return jsonify({
                "error": "internal_server_error",
                "request_id": request_id,
            }), 500