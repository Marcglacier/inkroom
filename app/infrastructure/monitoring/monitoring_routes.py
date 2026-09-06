# app/infrastructure/monitoring/monitoring_routes.py

from flask import Blueprint, jsonify

from app.infrastructure.monitoring.checks import (
    get_health_monitor,
)

monitoring_bp = Blueprint(
    "monitoring",
    __name__,
)


@monitoring_bp.get("/health/history")
def health_history():

    monitor = get_health_monitor()

    if monitor is None:
        return jsonify(
            {
                "history": [],
                "count": 0,
            }
        ), 200

    history = monitor.get_history()

    return jsonify(
        {
            "history": history,
            "count": len(history),
        }
    ), 200


@monitoring_bp.get("/health/summary")
def health_summary():

    monitor = get_health_monitor()

    if monitor is None:
        return jsonify({}), 200

    return jsonify(
        monitor.get_summary()
    ), 200


@monitoring_bp.get("/health/reliability")
def health_reliability():

    monitor = get_health_monitor()

    if monitor is None:
        return jsonify({}), 200

    return jsonify(
        monitor.get_reliability()
    ), 200


@monitoring_bp.get("/health/slo")
def health_slo():

    monitor = get_health_monitor()

    if monitor is None:
        return jsonify({}), 200

    return jsonify(
        monitor.get_availability_slo()
    ), 200


@monitoring_bp.get("/alerts")
def alerts():

    monitor = get_health_monitor()

    if monitor is None:
        return jsonify(
            {
                "alerts": [],
                "count": 0,
            }
        ), 200

    alerts = monitor.get_alerts()

    return jsonify(
        {
            "alerts": alerts,
            "count": len(alerts),
        }
    ), 200


@monitoring_bp.get("/errors")
def errors():

    monitor = get_health_monitor()

    if monitor is None:
        return jsonify(
            {
                "errors": [],
                "count": 0,
            }
        ), 200

    errors = monitor.get_errors()

    return jsonify(
        {
            "errors": errors,
            "count": len(errors),
        }
    ), 200