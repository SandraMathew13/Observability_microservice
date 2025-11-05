# metrics_service.py
import threading
import time
import psutil
from datetime import datetime
from database import insert_alert, insert_metric

class MetricsCollector:
    def __init__(self, interval=5, cpu_threshold=80.0, mem_threshold=75.0):
        self.interval = interval
        self.cpu_threshold = cpu_threshold
        self.mem_threshold = mem_threshold
        self._stop = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self.thread.start()

    def stop(self):
        self._stop.set()
        self.thread.join(timeout=2)

    def _run(self):
        while not self._stop.is_set():
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().percent
            ts = datetime.utcnow().isoformat()
            insert_metric("CPU", cpu, ts)
            insert_metric("Memory", mem, ts)
            # generate alerts
            if cpu > self.cpu_threshold:
                insert_alert("CPU", cpu, ts)
            if mem > self.mem_threshold:
                insert_alert("Memory", mem, ts)
            time.sleep(self.interval)
