"""Typed request and response models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=300)
    focus: str = Field(default="技术趋势与落地建议", max_length=200)
    max_sources: int = Field(default=4, ge=1, le=6)


class Source(BaseModel):
    id: str
    title: str
    publisher: str
    year: int
    excerpt: str
    relevance: float


class TraceStep(BaseModel):
    agent: str
    status: str
    detail: str


class ResearchResponse(BaseModel):
    topic: str
    focus: str
    summary: str
    sections: list[str]
    sources: list[Source]
    trace: list[TraceStep]
    mode: str = "offline_corpus"
