# app/infrastructure/database/metrics/database_metrics.py

import logging

from sqlalchemy import text

from app.extensions import db


logger = logging.getLogger("inkroom.database")


class DatabaseMetrics:

    @staticmethod
    def get_connection_metrics() -> dict:

        try:
            max_connections = db.session.execute(
                text("SHOW max_connections")
            ).scalar()

            current_connections = db.session.execute(
                text("""
                    SELECT count(*)
                    FROM pg_stat_activity
                """)
            ).scalar()

            active_connections = db.session.execute(
                text("""
                    SELECT count(*)
                    FROM pg_stat_activity
                    WHERE state = 'active'
                """)
            ).scalar()

            idle_connections = db.session.execute(
                text("""
                    SELECT count(*)
                    FROM pg_stat_activity
                    WHERE state = 'idle'
                """)
            ).scalar()

            return {
                "max_connections": int(max_connections),
                "current_connections": int(current_connections),
                "active_connections": int(active_connections),
                "idle_connections": int(idle_connections),
            }

        except Exception:

            db.session.rollback()

            logger.exception(
                "Failed to collect database connection metrics"
            )

            raise

    @staticmethod
    def get_pool_metrics() -> dict:

        try:
            engine = db.engine
            pool = engine.pool

            return {
                "pool_size": pool.size(),
                "checked_in": pool.checkedin(),
                "checked_out": pool.checkedout(),
                "overflow": pool.overflow(),
                "max_capacity": (
                    pool.size()
                    + pool._max_overflow
                ),
            }

        except Exception:

            logger.exception(
                "Failed to collect database pool metrics"
            )

            raise

    @classmethod
    def collect(cls) -> dict:

        return {
            "database": cls.get_connection_metrics(),
            "pool": cls.get_pool_metrics(),
        }