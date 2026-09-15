"""A deterministic planner/researcher/critic/synthesizer pipeline."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .models import ResearchResponse, Source, TraceStep


@dataclass(frozen=True)
class CorpusItem:
    id: str
    title: str
    publisher: str
    year: int
    excerpt: str
    keywords: tuple[str, ...]


CORPUS = (
    CorpusItem(
        "R1",
        "RAG evaluation: from answer quality to retrieval diagnostics",
        "AI Engineering Notes",
        2025,
        "可靠的 RAG 评估需要把召回、证据覆盖、答案忠实度和引用正确性拆开测量，而不是只看一个总分。",
        ("rag", "retrieval", "evaluation", "evidence", "召回", "评估", "引用"),
    ),
    CorpusItem(
        "R2",
        "Building reliable tool-using agents",
        "Agent Systems Review",
        2025,
        "工具型 Agent 的工程重点包括清晰的工具契约、参数校验、可观测轨迹、失败恢复和人工接管边界。",
        ("agent", "tool", "reliability", "observability", "工具", "智能体", "可靠性"),
    ),
    CorpusItem(
        "R3",
        "MCP as an integration boundary for AI applications",
        "Developer Platform Lab",
        2024,
        "将外部能力封装为明确的 MCP 工具，可以把 Agent 推理与服务实现解耦，但仍需关注权限、超时和数据最小化。",
        ("mcp", "integration", "tools", "security", "工具", "集成", "权限"),
    ),
    CorpusItem(
        "R4",
        "Human-in-the-loop patterns for customer-facing AI",
        "Product AI Journal",
        2024,
        "面向用户的 AI 系统应在高风险、不确定和缺少证据时转人工，并保留上下文、理由和审计事件。",
        ("human", "handoff", "safety", "customer", "人工", "客服", "安全", "接管"),
    ),
    CorpusItem(
        "R5",
        "Offline-first prototyping for LLM products",
        "Applied AI Practice",
        2025,
        "确定性离线替身可以先验证 API 合约、状态流转、错误处理和 UI，再接入真实模型与外部服务。",
        ("offline", "prototype", "testing", "llm", "离线", "原型", "测试", "大模型"),
    ),
)


def _terms(text: str) -> set[str]:
    lowered = text.lower()
    words = set(re.findall(r"[a-z0-9]+", lowered))
    words.update(char for char in lowered if "\u4e00" <= char <= "\u9fff")
    return words


class ResearchService:
    """Runs a small multi-agent research graph over a local corpus."""

    def __init__(self, corpus: tuple[CorpusItem, ...] = CORPUS) -> None:
        self.corpus = corpus

    def _retrieve(self, topic: str, focus: str, limit: int) -> list[Source]:
        query_terms = _terms(f"{topic} {focus}")
        ranked: list[tuple[int, CorpusItem]] = []
        for item in self.corpus:
            score = len(query_terms.intersection(_terms(" ".join(item.keywords))))
            ranked.append((score, item))
        ranked.sort(key=lambda pair: (-pair[0], pair[1].id))
        selected = ranked[:limit]
        maximum = max((score for score, _ in selected), default=1)
        return [
            Source(
                id=item.id,
                title=item.title,
                publisher=item.publisher,
                year=item.year,
                excerpt=item.excerpt,
                relevance=round(score / maximum, 2) if score else 0.1,
            )
            for score, item in selected
        ]

    def research(self, topic: str, focus: str = "技术趋势与落地建议", max_sources: int = 4) -> ResearchResponse:
        cleaned_topic = topic.strip()
        cleaned_focus = focus.strip() or "技术趋势与落地建议"
        if len(cleaned_topic) < 2:
            raise ValueError("topic 至少需要 2 个字符")
        if len(cleaned_topic) > 300:
            raise ValueError("topic 不能超过 300 个字符")
        sources = self._retrieve(cleaned_topic, cleaned_focus, max_sources)
        plan = ["定义研究问题", "检索候选证据", "批评证据覆盖", "综合结论与建议"]
        trace = [
            TraceStep(agent="planner", status="done", detail="；".join(plan)),
            TraceStep(agent="researcher", status="done", detail=f"selected_sources={len(sources)}"),
            TraceStep(agent="critic", status="done" if sources else "warning", detail="每条结论绑定本地来源" if sources else "没有命中高相关来源"),
        ]
        citations = "、".join(f"[{source.id}]" for source in sources)
        summary = f"围绕“{cleaned_topic}”的离线研究表明：优先建立可评估、可观测、可回退的应用链路，再逐步接入真实模型和外部数据。核心依据来自 {citations or '离线工程原则'}。"
        sections = [
            f"研究问题：{cleaned_topic}（关注：{cleaned_focus}）。本次流程由 planner 拆解问题，researcher 从本地语料挑选证据，critic 检查覆盖，synthesizer 生成结论。",
            "关键发现：" + "；".join(f"{source.title}：{source.excerpt}[{source.id}]" for source in sources),
            f"落地建议：先用离线替身验证数据结构、接口、评测和失败边界；上线前再补充真实来源、权限、时效性检查和人工复核。引用集合：{citations or '暂无'}。",
        ]
        trace.append(TraceStep(agent="synthesizer", status="done", detail=f"sections={len(sections)}; citations={len(sources)}"))
        return ResearchResponse(topic=cleaned_topic, focus=cleaned_focus, summary=summary, sections=sections, sources=sources, trace=trace)
