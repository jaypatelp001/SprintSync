"""Metrics router — Prometheus-style JSON metrics endpoint."""

import time
from collections import defaultdict
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task import Task, TaskStatus
from app.models.user import User

router = APIRouter(tags=["Observability"])

# In-memory metrics counters (reset on restart — fine for MVP)
_metrics = {
    "requests_total": defaultdict(int),
    "request_latency_seconds": [],
    "start_time": time.time(),
}


def record_request(method: str, path: str, status_code: int, latency_s: float):
    """Record a request in the metrics store (called from middleware)."""
    key = f"{method} {path} {status_code}"
    _metrics["requests_total"][key] += 1
    _metrics["request_latency_seconds"].append(latency_s)


@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    """Prometheus-style JSON metrics endpoint.

    Returns request counters, latency stats, and application-level gauges.
    """
    latencies = _metrics["request_latency_seconds"]
    uptime = time.time() - _metrics["start_time"]

    # Application gauges
    total_users = db.query(User).count()
    total_tasks = db.query(Task).count()
    tasks_by_status = {}
    for status in TaskStatus:
        count = db.query(Task).filter(Task.status == status).count()
        tasks_by_status[status.value] = count

    # Latency histogram buckets
    buckets = [0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
    histogram = {f"le_{b}": sum(1 for l in latencies if l <= b) for b in buckets}
    histogram["count"] = len(latencies)
    histogram["sum"] = round(sum(latencies), 4) if latencies else 0

    return {
        "uptime_seconds": round(uptime, 2),
        "requests_total": dict(_metrics["requests_total"]),
        "request_latency_seconds": histogram,
        "gauges": {
            "active_users": total_users,
            "total_tasks": total_tasks,
            "tasks_by_status": tasks_by_status,
        },
    }
