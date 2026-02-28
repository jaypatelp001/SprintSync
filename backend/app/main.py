"""SprintSync — FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth

# Create tables on startup (dev convenience — migrations handle production)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SprintSync API",
    description="Lean internal tool for logging work, tracking time, and AI-powered planning.",
    version="0.3.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Register Routers ---
app.include_router(auth.router)


@app.get("/", tags=["Root"])
def root():
    """Health check / welcome endpoint."""
    return {
        "app": "SprintSync",
        "version": "0.3.0",
        "status": "running",
        "docs": "/docs",
    }
