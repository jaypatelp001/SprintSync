"""SprintSync — FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth, users, tasks, ai, metrics, stats
from app.middleware.logging import RequestLoggingMiddleware

# Create tables on startup (dev convenience — migrations handle production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SprintSync API",
    description="Lean internal tool for logging work, tracking time, and AI-powered planning.",
    version="0.6.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# --- Middleware (order matters: last added = first executed) ---
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Set to False to allow "*" wildcard
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Register Routers ---
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(ai.router)
app.include_router(metrics.router)
app.include_router(stats.router)


@app.get("/", tags=["Root"])
def root():
    """Health check / welcome endpoint."""
    return {
        "app": "SprintSync",
        "version": "0.6.0",
        "status": "running",
        "docs": "/docs",
    }
