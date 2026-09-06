# app/infrastructure/monitoring/health_routes.py

from flask import Blueprint, jsonify

from app.infrastructure.monitoring.health_service import (
    HealthService,
)
from app.infrastructure.database.metrics import (
    DatabaseMetrics,
)
from app.infrastructure.monitoring.checks import (
    get_health_monitor,
)

health_bp = Blueprint(
    "health",
    __name__,
)


@health_bp.get("/health")
def health_check():

    result = HealthService().check()

    status_code = (
        200
        if result["status"] == "healthy"
        else 503
    )

    return jsonify(result), status_code

@health_bp.get("/health/database")
def database_health_metrics():

    return jsonify(
        DatabaseMetrics.get_connection_metrics()
    )

@health_bp.route("/health/live", methods=["GET"])
def health_live():
    return {
        "status": "alive"
    }, 200

@health_bp.route("/health/ready", methods=["GET"])
def health_ready():

    result = HealthService().check()

    ready = HealthService.is_ready(
        result
    )

    status_code = (
        200
        if ready
        else 503
    )

    return jsonify(
        {
            "status": (
                "ready"
                if ready
                else "not_ready"
            ),
            "checks": result,
        }
    ), status_code

