# app.py
from flask import Flask
from database import init_db
from auth_service import auth_bp, sessions

from reporting_service import report_bp
from metrics_service import MetricsCollector
from log_analyzer import analyze_log_file
import os

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(report_bp, url_prefix="/api")

# init database
init_db()

# start metrics collector
collector = MetricsCollector(interval=5, cpu_threshold=80.0, mem_threshold=75.0)
collector.start()

@app.route("/")
def home():
    return {"status": "observability service running"}

# small endpoint to run log analysis (for demo)
@app.route("/run-log-analysis", methods=["GET"])
def run_log_analysis():
    path = "sample_logs/system.log"
    if not os.path.exists(path):
        return {"error": "no sample log found"}, 404
    counts, top5 = analyze_log_file(path)
    return {"counts": counts, "top5_errors": top5}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
