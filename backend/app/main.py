"""
GlassBox — self-serve recovery potential preview.

A single FastAPI app that serves both the /api/estimate endpoint and
the static frontend (frontend/), so the whole demo runs from one
`uvicorn` process on one port.
"""

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .calculations import estimate_recovery
from .feed_generator import generate_sample_feed
from .models import EstimateRequest, EstimateResponse
from .sample_conversations import SAMPLE_CONVERSATIONS

# backend/app/main.py -> backend/app -> backend -> project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

app = FastAPI(
    title="GlassBox",
    description="Self-serve recovery potential preview for SmartRecover prospects.",
)

# Wide open for local demo use. If this is ever deployed publicly,
# tighten allow_origins to the actual frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ESTIMATE_DISCLAIMER = (
    "This is an illustrative estimate based on SmartRecover's published "
    "aggregate benchmarks. Actual results vary by funnel and are modeled "
    "precisely during your onboarding call."
)


@app.get("/health")
def health_check() -> dict:
    """Simple liveness check used during local development."""
    return {"status": "ok"}


@app.post("/api/estimate", response_model=EstimateResponse)
def create_estimate(payload: EstimateRequest) -> EstimateResponse:
    """
    Turn a handful of funnel numbers into a personalized, directional
    recovery estimate, a sample attribution feed, and a sample rep
    conversation for the selected funnel stage.
    """
    numbers = estimate_recovery(
        monthly_abandoned_leads=payload.monthly_abandoned_leads,
        average_order_value=payload.average_order_value,
        follow_up_method=payload.follow_up_method,
    )

    return EstimateResponse(
        **numbers,
        sample_feed=generate_sample_feed(average_order_value=payload.average_order_value),
        sample_conversation=SAMPLE_CONVERSATIONS[payload.funnel_stage],
        disclaimer=ESTIMATE_DISCLAIMER,
    )


# Mounted last and at "/" so it only catches requests that don't match
# an API route declared above (e.g. "/", "/styles.css", "/app.js").
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
