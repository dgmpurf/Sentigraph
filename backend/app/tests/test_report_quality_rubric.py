from app.schemas.report import PublicOpinionReport
from app.schemas.risk import TOPIC_RISK_MODEL_VERSION, TopicRiskScore
from app.services.evaluation.report_quality_rubric import evaluate_report_quality


def test_complete_report_passes_quality_rubric() -> None:
    report = _complete_report()

    result = evaluate_report_quality(
        report,
        expected_representative_comments=[
            "Quality issue remains unresolved.",
            "\u5b98\u65b9\u9700\u8981\u7ed9\u51fa\u660e\u786e\u65f6\u95f4\u8868\u3002",
        ],
    )

    assert result.grade == "pass"
    assert result.total_score >= 80
    assert 0 <= result.total_score <= 100
    assert set(result.dimension_scores) == {
        "completeness",
        "risk_explanation_quality",
        "actionability",
        "safety_professionalism",
        "language_formatting",
    }
    assert result.missing_sections == []


def test_missing_sections_reduce_report_quality_score() -> None:
    report = _complete_report().model_copy(update={"recommended_actions": []})

    result = evaluate_report_quality(report)

    assert result.grade == "warning"
    assert result.total_score < 100
    assert "missing_recommended_actions" in result.finding_codes()
    assert "recommended_actions" in result.missing_sections


def test_raw_json_dump_is_flagged() -> None:
    report = _complete_report().model_copy(update={"overall_summary": '{"risk": "high"}'})

    result = evaluate_report_quality(report)

    assert result.grade == "fail"
    assert "raw_json_dump" in result.finding_codes()
    assert 0 <= result.total_score <= 100


def test_vague_recommendations_are_warned() -> None:
    report = _complete_report().model_copy(
        update={
            "recommended_actions": ["Monitor.", "Follow up."],
            "suggested_public_response": "We care.",
        }
    )

    result = evaluate_report_quality(report)

    assert result.grade == "warning"
    assert "vague_recommendations" in result.finding_codes()
    assert "vague_public_response" in result.finding_codes()


def test_unsafe_overclaim_is_flagged() -> None:
    report = _complete_report().model_copy(
        update={
            "suggested_public_response": (
                "We confirmed fraud and criminal conduct before any verified review is complete."
            )
        }
    )

    result = evaluate_report_quality(report)

    assert result.grade == "fail"
    assert "unsupported_overclaim" in result.finding_codes()


def test_representative_comments_original_language_check_works() -> None:
    report = _complete_report().model_copy(update={"representative_comments": ["Quality issue remains unresolved."]})

    result = evaluate_report_quality(
        report,
        expected_representative_comments=[
            "Quality issue remains unresolved.",
            "\u5b98\u65b9\u9700\u8981\u7ed9\u51fa\u660e\u786e\u65f6\u95f4\u8868\u3002",
        ],
    )

    assert result.grade == "warning"
    assert "representative_comments_not_preserved" in result.finding_codes()


def test_markdown_expected_sections_check_works() -> None:
    report = _complete_report()
    markdown = "\n".join(
        [
            "# Offline report",
            "Risk 76/100 high",
            TOPIC_RISK_MODEL_VERSION,
            report.overall_summary,
            report.key_findings[0],
            report.top_risk_topics[0].topic,
            report.representative_comments[0],
            report.recommended_actions[0],
            report.suggested_public_response,
        ]
    )

    passing = evaluate_report_quality(
        report,
        markdown=markdown,
        required_markdown_sections=[
            "risk score",
            "risk level",
            "risk model version",
            "summary",
            "key findings",
            "top risk topics",
            "representative comments",
            "recommended actions",
            "suggested public response",
        ],
    )
    failing = evaluate_report_quality(
        report,
        markdown=markdown.replace(report.suggested_public_response, ""),
        required_markdown_sections=["suggested public response"],
    )

    assert passing.grade == "pass"
    assert "markdown_missing_sections" not in passing.finding_codes()
    assert "markdown_missing_sections" in failing.finding_codes()
    assert "markdown:suggested public response" in failing.missing_sections


def test_report_quality_score_stays_in_range_for_severely_bad_report() -> None:
    report = _complete_report().model_copy(
        update={
            "overall_summary": '{"secret": "sk-thisshouldnotappear"}',
            "key_findings": [],
            "main_risk_factors": [],
            "recommended_actions": [],
            "suggested_public_response": "We confirmed fraud.",
            "representative_comments": ["Contact: test@example.com"],
        }
    )

    result = evaluate_report_quality(report, expected_representative_comments=["missing comment"])

    assert result.grade == "fail"
    assert "secret_or_api_key_exposed" in result.finding_codes()
    assert "private_data_pattern" in result.finding_codes()
    assert 0 <= result.total_score <= 100


def _complete_report() -> PublicOpinionReport:
    topic = TopicRiskScore(
        topic_id="topic_001",
        cluster_id="topic_001",
        topic="Product quality issues",
        comment_count=12,
        negative_ratio=0.72,
        average_sentiment_score=-0.55,
        neg_severity=0.4,
        spread_signal=0.5,
        controversy_signal=0.2,
        bot_signal=0.1,
        influence_proxy=0.6,
        topic_risk_score=76.0,
        topic_risk_level="high",
        risk_explanation="Quality issue risk is elevated by negative sentiment and spread.",
        risk_score=76.0,
        risk_level="high",
    )
    return PublicOpinionReport(
        project_id="rubric_project",
        report_language="zh-CN",
        risk_score=76,
        risk_level="high",
        risk_level_label="\u9ad8\u98ce\u9669",
        risk_model_version=TOPIC_RISK_MODEL_VERSION,
        overall_summary=(
            "\u672c\u6b21\u79bb\u7ebf\u8bc4\u4f30\u663e\u793a\u9879\u76ee\u98ce\u9669\u4e3a"
            "\u9ad8\u98ce\u9669\uff0876/100\uff09\uff0c\u4e3b\u8981\u6765\u81ea\u4ea7\u54c1"
            "\u8d28\u91cf\u8bae\u9898\u548c\u7528\u6237\u6295\u8bc9\u6269\u6563\u3002"
        ),
        key_findings=[
            "V1.5 topic risk identifies Product quality issues as the leading topic.",
            "Real-crisis signal is 62.0/100 and manipulation signal is 21.0/100.",
        ],
        main_risk_factors=[
            "\u8d1f\u9762\u6295\u8bc9\u96c6\u4e2d\u5728Product quality issues\uff0c\u9700\u8981\u4e8b\u5b9e\u6027\u56de\u5e94\u3002",
        ],
        top_negative_topics=["Product quality issues: 12 comments"],
        representative_comments=[
            "Quality issue remains unresolved.",
            "\u5b98\u65b9\u9700\u8981\u7ed9\u51fa\u660e\u786e\u65f6\u95f4\u8868\u3002",
        ],
        suspected_bot_signals=["No strong repeated-script signal crossed the mock threshold."],
        recommended_actions=[
            "\u6307\u5b9a\u8d1f\u8d23\u4eba\u572824\u5c0f\u65f6\u5185\u6838\u5b9e\u8d28\u91cf\u95ee\u9898\u5e76\u51c6\u5907\u4e8b\u5b9e\u8bf4\u660e\u3002",
            "\u5ba2\u670d\u548c\u793e\u5a92\u56e2\u961f\u540c\u6b65\u53ef\u6838\u9a8c\u5904\u7406\u8fdb\u5c55\u548c\u652f\u6301\u6e20\u9053\u3002",
        ],
        suggested_public_response=(
            "\u6211\u4eec\u5df2\u5173\u6ce8\u5230\u76f8\u5173\u8ba8\u8bba\uff0c\u6b63\u5728\u6838\u5b9e"
            "\u4fe1\u606f\uff0c\u5e76\u5c06\u901a\u8fc7\u5b98\u65b9\u6e20\u9053\u53d1\u5e03\u53ef\u6838\u9a8c\u8fdb\u5c55\u3002"
        ),
        generated_from_mock_pipeline=True,
        topic_risks=[topic],
        top_risk_topics=[topic],
        max_topic_risk=76.0,
        average_topic_risk=52.0,
        overall_risk=68.0,
        real_crisis_risk=62.0,
        manipulation_risk=21.0,
        risk_explanation="V1.5 topic risk is elevated by Product quality issues.",
    )
