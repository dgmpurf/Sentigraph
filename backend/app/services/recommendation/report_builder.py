from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any

from app.schemas.analysis import AnalysisResultResponse, BotScore, RiskBrief, TopicCluster
from app.schemas.common import RISK_MODEL_VERSION, get_risk_level_label
from app.schemas.propagation import PropagationResponse
from app.schemas.report import PublicOpinionReport, ReportLanguage
from app.schemas.risk import TopicRiskScore, TopicRiskScoreResult
from app.schemas.visualization import VisualizationResponse


def build_public_opinion_report(
    analysis: AnalysisResultResponse,
    *,
    visualization: VisualizationResponse | None = None,
    propagation: PropagationResponse | None = None,
    risk_factors: Any | None = None,
    topic_risk_result: TopicRiskScoreResult | None = None,
    representative_comments: list[str] | None = None,
    include_representative_comments: bool = True,
    user_type: str = "brand",
    tone: str = "professional",
    report_language: ReportLanguage = "zh-CN",
    generated_from_mock_pipeline: bool = True,
) -> PublicOpinionReport:
    """Build a deterministic offline public opinion report from pipeline outputs."""
    language = _normalize_language(report_language)
    effective_analysis = _analysis_with_topic_risk(analysis, topic_risk_result)
    factor_values = _risk_factor_values(risk_factors, visualization)
    top_negative_topics = _top_negative_topics(effective_analysis.topics, language)
    top_risk_topic_lines = _top_risk_topic_lines(topic_risk_result, language)
    bot_signals = _bot_signals(
        effective_analysis.bot_accounts,
        effective_analysis.bot_score.suspected_bot_comment_ratio,
        factor_values.get("bot_impact", 0.0),
        language,
    )
    comments = _representative_comments(
        explicit_comments=representative_comments or [],
        topics=effective_analysis.topics,
        include=include_representative_comments,
    )
    main_risk_factors = _main_risk_factors(
        effective_analysis,
        factor_values,
        visualization,
        propagation,
        language,
        topic_risk_result=topic_risk_result,
    )
    actions = _recommended_actions(
        risk_level=effective_analysis.risk.risk_level,
        factors=factor_values,
        top_negative_topics=top_negative_topics,
        bot_signals=bot_signals,
        user_type=user_type,
        language=language,
    )
    key_findings = _key_findings(main_risk_factors, top_negative_topics, bot_signals, language)
    key_findings = _dedupe_preserve_order(top_risk_topic_lines + key_findings)[:8]

    return PublicOpinionReport(
        project_id=effective_analysis.project_id,
        report_language=language,
        risk_score=effective_analysis.risk.risk_score,
        risk_level=effective_analysis.risk.risk_level,
        risk_level_label=get_risk_level_label(effective_analysis.risk.risk_level, language),
        risk_model_version=topic_risk_result.risk_model_version if topic_risk_result else RISK_MODEL_VERSION,
        overall_summary=_overall_summary(effective_analysis, factor_values, visualization, propagation, language),
        key_findings=key_findings,
        main_risk_factors=main_risk_factors,
        top_negative_topics=top_negative_topics,
        representative_comments=comments,
        suspected_bot_signals=bot_signals,
        recommended_actions=actions,
        suggested_public_response=_suggested_public_response(
            risk_level=effective_analysis.risk.risk_level,
            top_negative_topics=top_negative_topics,
            tone=tone,
            language=language,
        ),
        generated_from_mock_pipeline=generated_from_mock_pipeline,
    topic_risks=topic_risk_result.topic_risks if topic_risk_result else [],
        top_risk_topics=topic_risk_result.top_risk_topics if topic_risk_result else [],
        max_topic_risk=topic_risk_result.max_topic_risk if topic_risk_result else None,
        average_topic_risk=topic_risk_result.average_topic_risk if topic_risk_result else None,
        overall_risk=topic_risk_result.overall_risk if topic_risk_result else None,
        real_crisis_risk=topic_risk_result.real_crisis_risk if topic_risk_result else None,
        manipulation_risk=topic_risk_result.manipulation_risk if topic_risk_result else None,
        risk_explanation=topic_risk_result.risk_explanation if topic_risk_result else None,
    )


def _analysis_with_topic_risk(
    analysis: AnalysisResultResponse,
    topic_risk_result: TopicRiskScoreResult | None,
) -> AnalysisResultResponse:
    if not topic_risk_result:
        return analysis
    return analysis.model_copy(
        update={
            "risk": RiskBrief(
                risk_score=int(round(topic_risk_result.overall_risk)),
                risk_level=topic_risk_result.risk_level,
            )
        }
    )


def _overall_summary(
    analysis: AnalysisResultResponse,
    factor_values: dict[str, float],
    visualization: VisualizationResponse | None,
    propagation: PropagationResponse | None,
    language: ReportLanguage,
) -> str:
    leading_topic = analysis.topics[0].topic if analysis.topics else _text("general discussion", "综合讨论", language)
    trend_points = len(visualization.sentiment_trend) if visualization else 0
    graph_nodes = len(propagation.nodes) if propagation else len(visualization.propagation_graph.nodes) if visualization else 0

    if language == "zh-CN":
        return (
            f"本次离线模拟管线评估显示，项目 {analysis.project_id} 当前舆情风险为"
            f"{_risk_level_label(analysis.risk.risk_level, language)}（{analysis.risk.risk_score}/100）。"
            f"负面情绪占比为{_format_percent(analysis.sentiment.negative_ratio)}，"
            f"讨论焦点集中在「{leading_topic}」。"
            f"系统观察到{trend_points}个情绪时间桶和{graph_nodes}个传播节点。"
            f"主要风险压力来自{_dominant_factor_label(factor_values, language)}。"
        )

    return (
        f"Public opinion risk is {analysis.risk.risk_level} at {analysis.risk.risk_score}/100. "
        f"Negative sentiment is {_format_percent(analysis.sentiment.negative_ratio)}, "
        f"with the strongest discussion around {leading_topic}. "
        f"The offline mock pipeline observed {trend_points} sentiment time bucket(s) "
        f"and {graph_nodes} propagation node(s). "
        f"Key risk pressure is {_dominant_factor_label(factor_values, language)}."
    )


def _main_risk_factors(
    analysis: AnalysisResultResponse,
    factor_values: dict[str, float],
    visualization: VisualizationResponse | None,
    propagation: PropagationResponse | None,
    language: ReportLanguage,
    *,
    topic_risk_result: TopicRiskScoreResult | None = None,
) -> list[str]:
    factors: list[str] = []
    factors.extend(_topic_risk_factor_lines(topic_risk_result, language))
    if analysis.sentiment.negative_ratio >= 0.5:
        factors.append(
            _text(
                f"Negative sentiment is elevated at {_format_percent(analysis.sentiment.negative_ratio)}.",
                f"负面情绪占比较高，当前为{_format_percent(analysis.sentiment.negative_ratio)}。",
                language,
            )
        )
    elif analysis.sentiment.negative_ratio > 0:
        factors.append(
            _text(
                f"Negative sentiment is present at {_format_percent(analysis.sentiment.negative_ratio)}.",
                f"已出现负面情绪，当前占比为{_format_percent(analysis.sentiment.negative_ratio)}。",
                language,
            )
        )

    trend_signal = _sentiment_trend_signal(visualization, language)
    if trend_signal:
        factors.append(trend_signal)

    if factor_values.get("bot_impact", 0.0) >= 0.3:
        factors.append(
            _text(
                f"Bot-like comment impact is {_format_percent(factor_values['bot_impact'])}.",
                f"疑似机器人或重复话术评论影响为{_format_percent(factor_values['bot_impact'])}。",
                language,
            )
        )
    elif analysis.bot_score.suspected_bot_comment_ratio > 0:
        factors.append(
            _text(
                "Suspected automated participation is visible at "
                f"{_format_percent(analysis.bot_score.suspected_bot_comment_ratio)} of comments.",
                "已观察到疑似自动化参与信号，占评论量"
                f"{_format_percent(analysis.bot_score.suspected_bot_comment_ratio)}。",
                language,
            )
        )

    if factor_values.get("propagation_speed", 0.0) >= 0.5:
        factors.append(
            _text(
                f"Propagation speed is high at {_format_percent(factor_values['propagation_speed'])}.",
                f"传播速度信号较高，当前为{_format_percent(factor_values['propagation_speed'])}。",
                language,
            )
        )

    if factor_values.get("controversy", 0.0) >= 0.5:
        factors.append(
            _text(
                f"Controversy signal is {_format_percent(factor_values['controversy'])}.",
                f"争议信号为{_format_percent(factor_values['controversy'])}。",
                language,
            )
        )

    if propagation and propagation.metrics.breadth:
        factors.append(
            _text(
                f"Propagation breadth covers {propagation.metrics.breadth} public interaction node(s).",
                f"传播范围覆盖{propagation.metrics.breadth}个公开互动节点。",
                language,
            )
        )
    elif visualization and visualization.propagation_graph.nodes:
        factors.append(
            _text(
                "Visualization propagation graph includes "
                f"{len(visualization.propagation_graph.nodes)} node(s) and "
                f"{len(visualization.propagation_graph.edges)} edge(s).",
                "可视化传播图包含"
                f"{len(visualization.propagation_graph.nodes)}个节点和"
                f"{len(visualization.propagation_graph.edges)}条边。",
                language,
            )
        )

    if visualization and visualization.heatmap:
        peak = max(visualization.heatmap, key=lambda item: item.intensity)
        factors.append(
            _text(
                f"Conversation intensity peaks on {peak.platform} at {peak.time_bucket}.",
                f"讨论强度峰值出现在{peak.platform}的{peak.time_bucket}。",
                language,
            )
        )

    return _dedupe_preserve_order(factors)[:6] or [
        _text(
            "No major risk factor crossed the current mock threshold.",
            "当前模拟阈值下未发现突出的主要风险因素。",
            language,
        )
    ]


def _sentiment_trend_signal(visualization: VisualizationResponse | None, language: ReportLanguage) -> str:
    if not visualization or len(visualization.sentiment_trend) < 2:
        return ""

    first = visualization.sentiment_trend[0]
    last = visualization.sentiment_trend[-1]
    first_negative = _trend_negative_ratio(first.positive, first.neutral, first.negative)
    last_negative = _trend_negative_ratio(last.positive, last.neutral, last.negative)
    delta = last_negative - first_negative
    if delta >= 0.05:
        return _text(
            "Negative sentiment trend rose from "
            f"{_format_percent(first_negative)} to {_format_percent(last_negative)} across mock time buckets.",
            "负面情绪趋势在模拟时间桶内从"
            f"{_format_percent(first_negative)}上升至{_format_percent(last_negative)}。",
            language,
        )
    if delta <= -0.05:
        return _text(
            "Negative sentiment trend eased from "
            f"{_format_percent(first_negative)} to {_format_percent(last_negative)} across mock time buckets.",
            "负面情绪趋势在模拟时间桶内从"
            f"{_format_percent(first_negative)}回落至{_format_percent(last_negative)}。",
            language,
        )
    return ""


def _trend_negative_ratio(positive: int, neutral: int, negative: int) -> float:
    total = positive + neutral + negative
    if total <= 0:
        return 0.0
    return negative / total


def _top_negative_topics(topics: list[TopicCluster], language: ReportLanguage) -> list[str]:
    sorted_topics = sorted(
        topics,
        key=lambda topic: (topic.average_sentiment_score, -topic.comment_count, topic.topic),
    )
    negative_topics = [
        _topic_line(topic, language)
        for topic in sorted_topics
        if topic.average_sentiment_score < 0
    ]
    if negative_topics:
        return negative_topics[:3]

    return [
        _topic_line(topic, language)
        for topic in sorted(topics, key=lambda topic: (-topic.comment_count, topic.topic))[:3]
    ]


def _top_risk_topic_lines(
    topic_risk_result: TopicRiskScoreResult | None,
    language: ReportLanguage,
) -> list[str]:
    if not topic_risk_result:
        return []
    return [_topic_risk_line(topic, language) for topic in topic_risk_result.top_risk_topics[:3]]


def _topic_risk_factor_lines(
    topic_risk_result: TopicRiskScoreResult | None,
    language: ReportLanguage,
) -> list[str]:
    if not topic_risk_result or not topic_risk_result.top_risk_topics:
        return []

    leading = topic_risk_result.top_risk_topics[0]
    if language == "zh-CN":
        return [
            (
                f"V1.5话题风险模型识别到最高风险话题：{leading.topic}"
                f"（{leading.topic_risk_score:.1f}/100，{_risk_level_label(leading.topic_risk_level, language)}）。"
            ),
            (
                f"真实危机信号为{topic_risk_result.real_crisis_risk:.1f}/100，"
                f"操纵/重复话术信号为{topic_risk_result.manipulation_risk:.1f}/100。"
            ),
        ]

    return [
        (
            f"V1.5 topic risk identifies {leading.topic} as the highest-risk topic "
            f"({leading.topic_risk_score:.1f}/100, {leading.topic_risk_level})."
        ),
        (
            f"Real-crisis signal is {topic_risk_result.real_crisis_risk:.1f}/100; "
            f"manipulation/repeated-script signal is {topic_risk_result.manipulation_risk:.1f}/100."
        ),
    ]


def _topic_risk_line(topic: TopicRiskScore, language: ReportLanguage) -> str:
    if language == "zh-CN":
        return (
            f"高风险话题：{topic.topic}，风险{topic.topic_risk_score:.1f}/100，"
            f"等级{_risk_level_label(topic.topic_risk_level, language)}，"
            f"负面占比{_format_percent(topic.negative_ratio)}。"
        )
    return (
        f"High-risk topic: {topic.topic}, risk {topic.topic_risk_score:.1f}/100, "
        f"level {topic.topic_risk_level}, negative ratio {_format_percent(topic.negative_ratio)}."
    )


def _topic_line(topic: TopicCluster, language: ReportLanguage) -> str:
    if language == "zh-CN":
        return f"{topic.topic}：{topic.comment_count}条评论，平均情绪{topic.average_sentiment_score:.2f}"
    return (
        f"{topic.topic}: {topic.comment_count} comment(s), "
        f"average sentiment {topic.average_sentiment_score:.2f}"
    )


def _representative_comments(
    *,
    explicit_comments: list[str],
    topics: list[TopicCluster],
    include: bool,
) -> list[str]:
    if not include:
        return []

    candidates: list[str] = [comment for comment in explicit_comments if comment]
    for topic in topics:
        candidates.extend(comment for comment in topic.representative_comments if comment)

    return _dedupe_preserve_order(candidates)[:5]


def _bot_signals(
    bot_accounts: list[BotScore],
    suspected_bot_comment_ratio: float,
    bot_impact: float,
    language: ReportLanguage,
) -> list[str]:
    signals: list[str] = []
    if max(suspected_bot_comment_ratio, bot_impact) >= 0.3:
        signals.append(
            _text(
                "Repeated-script or suspicious coordination signals are elevated: "
                f"bot-like comment impact is {_format_percent(max(suspected_bot_comment_ratio, bot_impact))}.",
                "重复话术或疑似协同信号较高：疑似机器人评论影响为"
                f"{_format_percent(max(suspected_bot_comment_ratio, bot_impact))}。",
                language,
            )
        )
    elif suspected_bot_comment_ratio > 0:
        signals.append(
            _text(
                "Light suspected automation signal is visible: "
                f"{_format_percent(suspected_bot_comment_ratio)} of comments are bot-like.",
                f"存在轻微疑似自动化信号：{_format_percent(suspected_bot_comment_ratio)}的评论呈现机器人特征。",
                language,
            )
        )

    for account in sorted(bot_accounts, key=lambda item: item.bot_probability, reverse=True)[:3]:
        if account.bot_probability < 0.3:
            continue
        reasons = ", ".join(account.bot_reasons[:2])
        signals.append(
            _text(
                f"{account.author_id} has bot probability {_format_percent(account.bot_probability)}"
                f" due to {reasons}.",
                f"{account.author_id}的疑似机器人概率为{_format_percent(account.bot_probability)}，"
                "主要原因包括重复内容、发布频率或情绪一致性异常。",
                language,
            )
        )

    return signals or [
        _text(
            "No strong bot-like account signal crossed the mock threshold.",
            "当前模拟阈值下未发现强疑似机器人账号信号。",
            language,
        )
    ]


def _recommended_actions(
    *,
    risk_level: str,
    factors: dict[str, float],
    top_negative_topics: list[str],
    bot_signals: list[str],
    user_type: str,
    language: ReportLanguage,
) -> list[str]:
    if language == "zh-CN":
        actions = [
            "发布事实性监测说明，承认主要关切，避免放大未经证实的信息。",
            "为客服与社媒团队准备简明问答口径。",
        ]
        if risk_level in {"high", "critical"}:
            actions.insert(0, "启动危机响应负责人机制，并在24小时内准备对外更新窗口。")
        elif risk_level == "medium":
            actions.insert(0, "指定负责人持续观察议题，并准备当日回应草案。")

        if top_negative_topics:
            actions.append("围绕首要负面议题提供可核验事实、处理进展和支持渠道。")

        if factors.get("bot_impact", 0.0) >= 0.3 or any(_contains_bot_signal(signal) for signal in bot_signals):
            actions.append("先区分真实用户投诉与重复话术信号，再决定回应强度。")

        if factors.get("propagation_speed", 0.0) >= 0.5:
            actions.append("持续观察后续两个小时级时间桶，确认传播是否继续加速。")

        if user_type in {"public_figure", "artist", "influencer"}:
            actions.append("采用冷静克制的个人声明，避免与单个账号争辩。")
        else:
            actions.append("保持品牌回应克制、具体，并与客服和支持流程保持一致。")

        return _dedupe_preserve_order(actions)[:6]

    actions = [
        "Publish a factual monitoring note that acknowledges the main concern without amplifying speculation.",
        "Prepare a concise FAQ for customer service and social media teams.",
    ]

    if risk_level in {"high", "critical"}:
        actions.insert(0, "Escalate to the crisis response owner and set a 24-hour public update window.")
    elif risk_level == "medium":
        actions.insert(0, "Assign an owner to watch the topic and prepare a same-day response draft.")

    if top_negative_topics:
        actions.append("Address the leading negative topic directly with verifiable facts and support options.")

    if factors.get("bot_impact", 0.0) >= 0.3 or any(_contains_bot_signal(signal) for signal in bot_signals):
        actions.append("Separate organic complaints from repeated-script signals before deciding escalation tone.")

    if factors.get("propagation_speed", 0.0) >= 0.5:
        actions.append("Monitor the next two hourly buckets for acceleration before expanding the response scope.")

    if user_type in {"public_figure", "artist", "influencer"}:
        actions.append("Use a calm personal statement and avoid arguing with individual accounts.")
    else:
        actions.append("Keep the response brand-safe, specific, and aligned with support operations.")

    return _dedupe_preserve_order(actions)[:6]


def _suggested_public_response(
    *,
    risk_level: str,
    top_negative_topics: list[str],
    tone: str,
    language: ReportLanguage,
) -> str:
    topic_phrase = _text("the concerns being discussed", "相关讨论", language)
    if top_negative_topics:
        separator = "：" if language == "zh-CN" else ":"
        topic_phrase = top_negative_topics[0].split(separator, 1)[0]
        if language == "en-US":
            topic_phrase = topic_phrase.lower()

    if language == "zh-CN":
        opening = "我们已注意到近期关于"
        if tone == "empathetic":
            opening = "我们理解大家对"
        elif tone == "direct":
            opening = "我们已关注到"

        urgency = "目前我们正在核实相关信息，并会在有明确进展后及时通过官方渠道说明。"
        if risk_level in {"high", "critical"}:
            urgency = "我们已将相关情况列为优先处理事项，并将在确认事实后通过官方渠道持续更新。"

        return (
            f"{opening}{topic_phrase}的讨论。"
            f"{urgency}"
            "如用户有具体案例，欢迎通过官方客服或支持渠道提交信息，"
            "我们会基于事实进行核查和处理。"
        )

    opening = "We are aware of the recent discussion around"
    if tone == "empathetic":
        opening = "We understand the concern behind the recent discussion around"
    elif tone == "direct":
        opening = "We have seen the recent discussion around"

    urgency = "We are reviewing the information and will share verified updates as soon as possible."
    if risk_level in {"high", "critical"}:
        urgency = "We are prioritizing a review and will share verified updates within the next response window."

    return (
        f"{opening} {topic_phrase}. "
        f"{urgency} "
        "In the meantime, we encourage users to send specific cases through official support channels "
        "so they can be checked and handled accurately."
    )


def _key_findings(
    main_risk_factors: list[str],
    top_negative_topics: list[str],
    bot_signals: list[str],
    language: ReportLanguage,
) -> list[str]:
    topic_prefix = _text("Negative topic: ", "负面议题：", language)
    return _dedupe_preserve_order(
        main_risk_factors
        + [f"{topic_prefix}{topic}" for topic in top_negative_topics]
        + bot_signals
    )[:8]


def _risk_factor_values(
    risk_factors: Any | None,
    visualization: VisualizationResponse | None,
) -> dict[str, float]:
    if risk_factors is not None:
        if is_dataclass(risk_factors):
            raw = asdict(risk_factors)
        elif hasattr(risk_factors, "model_dump"):
            raw = risk_factors.model_dump()
        elif isinstance(risk_factors, dict):
            raw = risk_factors
        else:
            raw = {}

        return {
            "negative_sentiment": float(raw.get("negative_sentiment_ratio", 0.0)),
            "negative_strength": float(raw.get("negative_sentiment_strength", 0.0)),
            "bot_impact": float(raw.get("bot_impact_score", 0.0)),
            "propagation_speed": float(raw.get("propagation_speed", 0.0)),
            "controversy": float(raw.get("controversy_score", 0.0)),
            "trend_shift": float(raw.get("trend_shift", 0.0)),
        }

    if visualization:
        return {
            "negative_sentiment": float(visualization.risk_radar.negative_sentiment),
            "negative_strength": 0.0,
            "bot_impact": float(visualization.risk_radar.bot_impact),
            "propagation_speed": float(visualization.risk_radar.propagation_speed),
            "controversy": float(visualization.risk_radar.controversy),
            "trend_shift": float(visualization.risk_radar.trend_shift),
        }

    return {}


def _dominant_factor_label(factors: dict[str, float], language: ReportLanguage) -> str:
    labels = {
        "negative_sentiment": _text("negative sentiment", "负面情绪", language),
        "negative_strength": _text("negative sentiment strength", "负面情绪强度", language),
        "bot_impact": _text("bot-like amplification", "疑似机器人放大", language),
        "propagation_speed": _text("propagation speed", "传播速度", language),
        "controversy": _text("controversy", "争议程度", language),
        "trend_shift": _text("trend shift", "趋势变化", language),
    }
    if not factors:
        return _text("limited in the current mock data", "当前模拟数据中的信号有限", language)
    key, value = max(factors.items(), key=lambda item: item[1])
    if value <= 0:
        return _text("limited in the current mock data", "当前模拟数据中的信号有限", language)
    return f"{labels.get(key, key)}（{_format_percent(value)}）" if language == "zh-CN" else f"{labels.get(key, key)} ({_format_percent(value)})"


def _risk_level_label(risk_level: str, language: ReportLanguage) -> str:
    return get_risk_level_label(risk_level, language)


def _contains_bot_signal(value: str) -> bool:
    normalized = value.lower()
    return (
        "bot" in normalized
        or "automated" in normalized
        or "script" in normalized
        or "coordination" in normalized
        or "机器人" in value
        or "重复话术" in value
        or "协同" in value
    )


def _normalize_language(report_language: str) -> ReportLanguage:
    return "en-US" if report_language == "en-US" else "zh-CN"


def _text(en: str, zh: str, language: ReportLanguage) -> str:
    return zh if language == "zh-CN" else en


def _format_percent(value: float) -> str:
    return f"{round(value * 100)}%"


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped
