from deepresearch.service import ResearchService


def test_research_returns_sources_and_trace() -> None:
    result = ResearchService().research("RAG 评估", "召回与引用", 3)
    assert result.mode == "offline_corpus"
    assert result.sources[0].id == "R1"
    assert [step.agent for step in result.trace] == ["planner", "researcher", "critic", "synthesizer"]


def test_max_sources_is_respected() -> None:
    result = ResearchService().research("agent 工具", max_sources=2)
    assert len(result.sources) == 2


def test_unknown_topic_still_explains_evidence_boundary() -> None:
    result = ResearchService().research("火星农业", max_sources=2)
    assert len(result.sources) == 2
    assert "离线" in result.summary


def test_short_topic_is_rejected() -> None:
    try:
        ResearchService().research("A")
    except ValueError as error:
        assert "2 个字符" in str(error)
    else:
        raise AssertionError("short topic should fail")
