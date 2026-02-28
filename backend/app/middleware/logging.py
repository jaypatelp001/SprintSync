"""Structured request logging middleware — logs method, path, userId, latency, status."""

import time
import json
import logging
import traceback
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("sprintsync.requests")

# Configure structured JSON logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler()],
)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs every request with structured JSON fields."""

    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()

        # Extract user_id from JWT if present (best-effort, non-blocking)
        user_id = None
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            try:
                from app.services.auth_service import decode_token
                token = auth_header.split(" ")[1]
                payload = decode_token(token)
                user_id = payload.get("sub")
            except Exception:
                pass  # Don't block the request for logging

        try:
            response = await call_next(request)
            latency_ms = round((time.time() - start_time) * 1000, 2)

            log_entry = {
                "level": "INFO",
                "method": request.method,
                "path": str(request.url.path),
                "query": str(request.url.query) if request.url.query else None,
                "status_code": response.status_code,
                "user_id": user_id,
                "latency_ms": latency_ms,
                "client_ip": request.client.host if request.client else None,
            }
            logger.info(json.dumps(log_entry))
            return response

        except Exception as exc:
            latency_ms = round((time.time() - start_time) * 1000, 2)

            error_entry = {
                "level": "ERROR",
                "method": request.method,
                "path": str(request.url.path),
                "user_id": user_id,
                "latency_ms": latency_ms,
                "error": str(exc),
                "stack_trace": traceback.format_exc(),
            }
            logger.error(json.dumps(error_entry))
            raise
