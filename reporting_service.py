# reporting_service.py
from flask import Blueprint, jsonify, request
from database import get_last_n_alerts, get_alert_stats, get_last_metrics
from auth_service import validate_token_from_header

report_bp = Blueprint("report", __name__)

@report_bp.route("/summary", methods=["GET"])
def summary():
    # token check
    token = validate_token_from_header(request.headers)
    if not token:
        return jsonify({"error": "unauthorized"}), 401

    total, cpu_count, mem_count = get_alert_stats()
    last_alerts = get_last_n_alerts(10)
    cpu_last10 = get_last_metrics("CPU", 10)
    mem_last10 = get_last_metrics("Memory", 10)
    def avg(lst):
        return sum(lst)/len(lst) if lst else None
    resp = {
        "total_alerts": total or 0,
        "breakdown": {"CPU": cpu_count or 0, "Memory": mem_count or 0},
        "last_alerts": [{"type": t, "value": v, "timestamp": ts} for (t, v, ts) in last_alerts],
        "average_metrics": {"CPU": avg(cpu_last10), "Memory": avg(mem_last10)}
    }
    return jsonify(resp)
