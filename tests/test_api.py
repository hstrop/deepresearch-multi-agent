from fastapi.testclient import TestClient

from deepresearch.api import create_app


def test_health_and_research_api() -> None:
    with TestClient(create_app()) as client:
        assert client.get("/health").json()["mode"] == "offline_corpus"
        response = client.post("/v1/research", json={"topic": "MCP 工具集成", "max_sources": 2})
    assert response.status_code == 200
    assert response.json()["sources"][0]["id"] == "R3"


def test_api_rejects_empty_topic() -> None:
    with TestClient(create_app()) as client:
        response = client.post("/v1/research", json={"topic": ""})
    assert response.status_code == 422


def test_api_rejects_too_many_sources() -> None:
    with TestClient(create_app()) as client:
        response = client.post("/v1/research", json={"topic": "RAG", "max_sources": 7})
    assert response.status_code == 422
