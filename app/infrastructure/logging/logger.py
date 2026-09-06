# app/infrastructure/logging/logger.py

import logging
import sys

from .request_context import get_request_id


class RequestIdFilter(logging.Filter):
    """
    Injects the current request ID into every log record.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id() or "-"
        return True


class SafeFormatter(logging.Formatter):
    """
    Makes sure logs that don't originate from our application
    still have the fields expected by the formatter.
    """

    def format(self, record: logging.LogRecord) -> str:
        if not hasattr(record, "request_id"):
            record.request_id = get_request_id() or "-"

        return super().format(record)


def configure_logging() -> None:
    """
    Configure InkRoom's application logging.
    """

    root_logger = logging.getLogger()

    root_logger.setLevel(logging.INFO)

    # ------------------------------------------------------------
    # Do not destroy existing handlers.
    #
    # Celery configures its own logging handlers before tasks run.
    # Clearing them from inside create_app() can interfere with the
    # Celery worker's logging lifecycle.
    # ------------------------------------------------------------

    if not root_logger.handlers:

        handler = logging.StreamHandler(sys.stdout)

        formatter = SafeFormatter(
            "%(asctime)s | "
            "%(levelname)s | "
            "request_id=%(request_id)s | "
            "%(name)s | "
            "%(message)s"
        )

        handler.setFormatter(formatter)
        handler.addFilter(RequestIdFilter())

        root_logger.addHandler(handler)

    # Keep Werkzeug access logs.
    logging.getLogger("werkzeug").setLevel(logging.INFO)