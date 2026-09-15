"""FastAPI entry point for DeepResearch."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .models import ResearchRequest, ResearchResponse
from .service import ResearchService


def create_app() -> FastAPI:
    application = FastAPI(
        title="DeepResearch Multi-Agent API",
        version="0.1.0",
        description="Offline-first multi-agent research workflow with source-aware synthesis",
    )
    application.state.service = ResearchService()
    static_dir = Path(__file__).parent / "static"
    application.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")

    @application.get("/", include_in_schema=False)
    async def frontend() -> FileResponse:
        return FileResponse(static_dir / "index.html")

    @application.get("/health")
    async def health() -> dict[str, object]:
        return {"status": "ok", "mode": "offline_corpus", "corpus_size": len(application.state.service.corpus)}

    @application.post("/v1/research", response_model=ResearchResponse)
    async def research(payload: ResearchRequest, request: Request) -> ResearchResponse:
        try:
            return request.app.state.service.research(payload.topic, payload.focus, payload.max_sources)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    return application


app = create_app()
