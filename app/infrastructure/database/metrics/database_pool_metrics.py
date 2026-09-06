# app/infrastructure/database/metrics/database_pool_metrics.py

import logging

from app.extensions import db


logger = logging.getLogger(
    "inkroom.database"
)


class DatabasePoolMetrics:

    def get_pool_metrics(self) -> dict:

        try:

            pool = db.engine.pool

            pool_size = pool.size()

            checked_out = pool.checkedout()

            checked_in = pool.checkedin()

            max_overflow = pool._max_overflow

            max_capacity = (
                pool_size
                + max_overflow
            )

            available_capacity = max(
                max_capacity - checked_out,
                0,
            )

            return {
                "pool_size": pool_size,
                "max_overflow": max_overflow,
                "max_capacity": max_capacity,
                "checked_out": checked_out,
                "checked_in": checked_in,
                "available_capacity": (
                    available_capacity
                ),
            }

        except Exception:

            logger.exception(
                "Failed to collect SQLAlchemy pool metrics"
            )

            return {
                "pool_size": None,
                "max_overflow": None,
                "max_capacity": None,
                "checked_out": None,
                "checked_in": None,
                "available_capacity": None,
            }

