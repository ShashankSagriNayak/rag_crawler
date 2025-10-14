import json
import os
import time


class MetricsLogger:
    def __init__(self, log_path="data/logs/metrics.jsonl"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def log(self, query, timings, answer_status="success"):
        entry = {
            "timestamp": time.time(),
            "query": query,
            "timings": timings,
            "status": answer_status,
        }
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
