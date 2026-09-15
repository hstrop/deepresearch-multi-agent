# DeepResearch Multi-Agent

DeepResearch is an offline-first multi-agent industry research prototype. It turns a research request into a visible workflow: planner → researcher → critic → synthesizer, with source-aware sections and an auditable trace.

## Global AI/LLM Internship Portfolio

The project demonstrates how to make multi-agent research explainable before adding live search. The deterministic local corpus makes API contracts, source selection, evidence coverage, synthesis, and UI states testable without network access.

**Engineering signals:** Python · FastAPI · multi-agent orchestration · source-aware synthesis · evidence boundaries · deterministic evaluation · responsive research UI.

This is an offline research fixture, not a real-time market intelligence product. A web search connector, document store, citation verifier, and freshness policy can be attached behind the existing `ResearchService` boundary.

## Features

- Four explicit roles: planner, researcher, critic, and synthesizer.
- Relevance-ranked local sources with publisher, year, excerpt, and citation ID.
- Research summary, structured sections, source cards, and agent trace in one response.
- Configurable focus and source limit with FastAPI validation.
- No API key, external search, or live-data claim in the default mode.

## Quick start

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
.\run_demo.ps1
```

Open `http://127.0.0.1:8030/`; API docs are at `http://127.0.0.1:8030/docs`.

## Verification

```powershell
$env:PYTHONPATH = "src"
python -m pytest -q
```

The suite covers agent ordering, source limits, unknown-topic boundaries, request validation, and health behavior.
