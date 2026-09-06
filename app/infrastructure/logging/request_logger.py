# app/infrastructure/logging/request_logger.py
import logging
import time
from flask import request
from .request_context import get_request_id

logger = logging.getLogger("inkroom.request")


class RequestLogger:

    @staticmethod
    def start() -> float:
        return time.perf_counter()

    @staticmethod
    def finish(
        started_at: float,
        status_code: int,
    ) -> None:

        duration_ms = (
            time.perf_counter() - started_at
        ) * 1000

        logger.info(
            "HTTP %s %s | status=%s | duration=%.2fms",
            request.method,
            request.path,
            status_code,
            duration_ms,
        )