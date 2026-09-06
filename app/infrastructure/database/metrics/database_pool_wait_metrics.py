# app/infrastructure/database/metrics/database_pool_wait_metrics.py

import logging
import time

from sqlalchemy import text

from app.extensions import db


logger = logging.getLogger(
    "inkroom.database"
)


class DatabasePoolWaitMetrics:

    def measure(self) -> dict:

        started_at = time.perf_counter()

        try:

            db.session.execute(
                text("SELECT 1")
            )

            duration_ms = (
                time.perf_counter()
                - started_at
            ) * 1000

            return {
                "wait_time_ms": round(
                    duration_ms, 2,
                ),
            }

        except Exception:

            duration_ms = (
                time.perf_counter()
                - started_at
            ) * 1000

            logger.exception(
                "Database connection acquisition failed"
            )

            return {
                "wait_time_ms": None,
            }

