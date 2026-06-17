import {
  App as AntApp,
  Alert,
  Button,
  Card,
  Col,
  Empty,
  List,
  Progress,
  Row,
  Skeleton,
  Space,
  Table,
  Tag,
  Typography,
} from 'antd'
import { useMemo } from 'react'
import {
  AlertTriangle,
  Bot,
  ClipboardCopy,
  FileText,
  Lightbulb,
  MessageCircleWarning,
  MessageSquareText,
  ShieldAlert,
  Target,
} from 'lucide-react'

import { SentimentTrendChart } from '../components/charts/SentimentTrendChart.jsx'
import { copyTextToClipboard } from '../utils/clipboard.js'
import { getAnalysisSourceStatus } from '../utils/dataSourceStatus.js'
import { formatPercent, riskTone } from '../utils/formatters.js'
import { buildPublicOpinionReportModel, hasReportContent } from '../utils/reportModel.js'

const { Paragraph, Text, Title } = Typography

const riskLevelLabels = {
  low: '低风险',
  medium: '中等风险',
  high: '高风险',
  critical: '严重风险',
}

const topicColumns = [
  {
    title: '话题',
    dataIndex: 'topic',
    key: 'topic',
    width: 220,
    render: (value, record) => (
      <Space direction="vertical" size={2}>
        <Text strong>{value || '未命名话题'}</Text>
        <Text type="secondary">{record.cluster_id || record.topic_id || '-'}</Text>
      </Space>
    ),
  },
  { title: '评论数', dataIndex: 'comment_count', key: 'comment_count', width: 110 },
  {
    title: '平均情绪',
    dataIndex: 'average_sentiment_score',
    key: 'average_sentiment_score',
    width: 130,
    render: (value) => {
      const numericValue = Number(value || 0)
      return <Tag color={numericValue < 0 ? 'error' : numericValue > 0 ? 'success' : 'default'}>{numericValue.toFixed(2)}</Tag>
    },
  },
  { title: '摘要', dataIndex: 'summary', key: 'summary', render: (value) => value || '暂无摘要' },
]

function scoreText(value) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue.toFixed(1) : '0.0'
}

function SentimentBar({ color, label, value }) {
  return (
    <div className="sentiment-bar-row">
      <Space className="full-width" direction="vertical" size={4}>
        <Space className="sentiment-bar-label">
          <Text>{label}</Text>
          <Text strong>{formatPercent(value)}</Text>
        </Space>
        <Progress percent={Math.round((value || 0) * 100)} showInfo={false} strokeColor={color} trailColor="#283043" />
      </Space>
    </div>
  )
}

function InsightList({ emptyText, items }) {
  return (
    <List
      dataSource={items}
      locale={{ emptyText }}
      renderItem={(item) => (
        <List.Item>
          <Text>{item}</Text>
        </List.Item>
      )}
    />
  )
}

function TopicRiskCards({ items }) {
  return (
    <List
      className="topic-risk-card-list"
      dataSource={items}
      grid={{ gutter: 12, column: 1 }}
      locale={{ emptyText: '暂无 V1.5 话题风险数据' }}
      renderItem={(item) => {
        const riskScore = Number(item.riskScore || 0)
        return (
          <List.Item>
            <div className={`topic-risk-card risk-${item.riskLevel}`}>
              <Space direction="vertical" className="full-width" size={10}>
                <Space className="analysis-signal-line" wrap>
                  <Text strong>{item.topic}</Text>
                  <Tag color={riskTone(item.riskLevel)}>{riskLevelLabels[item.riskLevel] || item.riskLevel}</Tag>
                  <Tag color="volcano">话题风险分 {scoreText(riskScore)}/100</Tag>
                </Space>
                <Progress percent={Math.round(riskScore)} showInfo={false} strokeColor="#ff5d8f" trailColor="#283043" />
                <Text type="secondary">主要驱动因素</Text>
                <div className="topic-risk-meta-grid">
                  <span>评论数：{item.commentCount || 0}</span>
                  <span>负面占比：{formatPercent(item.negativeRatio || 0)}</span>
                  <span>扩散信号：{formatPercent(item.spreadSignal || 0)}</span>
                  <span>操纵信号：{formatPercent(item.botSignal || 0)}</span>
                </div>
                <Paragraph className="topic-risk-explanation">
                  <Text type="secondary">风险解释：</Text>
                  {item.explanation || '暂无风险解释。'}
                </Paragraph>
              </Space>
            </div>
          </List.Item>
        )
      }}
    />
  )
}

function buildEvidenceSummary({ analysis, currentCase }) {
  const items = Array.isArray(currentCase?.evidence_items) ? currentCase.evidence_items : []
  const analysisSources = analysis?.evidence_source_distribution || {}
  const analysisTypes = analysis?.evidence_type_counts || {}
  const acquisitionModes = {}
  const trustLabels = {}
  const verificationStatuses = {}
  const provenanceTypes = {}
  const reviewStatuses = {}
  const riskFlags = {}
  const itemSources = {}
  const itemTypes = {}
  const titles = []
  const comments = []
  let sourceUrlPresent = 0
  let sourceUrlMissing = 0
  let reviewNeeded = Number(analysis?.evidence_review_needed_count || 0)
  let duplicateItems = Number(analysis?.evidence_duplicate_item_count || 0)
  for (const item of items) {
    if (item.title && !titles.includes(item.title)) titles.push(item.title)
    const comment = item.comment_text || item.body_text
    if (comment && !comments.includes(comment)) comments.push(comment)
    const acquisitionMode = item.acquisition_mode || 'unknown'
    acquisitionModes[acquisitionMode] = (acquisitionModes[acquisitionMode] || 0) + 1
    const trustLabel = item.trust_label || 'unknown'
    const verificationStatus = item.verification_status || 'unknown'
    const provenanceType = item.provenance_type || 'unknown'
    const reviewStatus = item.review_status || 'not_reviewed'
    trustLabels[trustLabel] = (trustLabels[trustLabel] || 0) + 1
    verificationStatuses[verificationStatus] = (verificationStatuses[verificationStatus] || 0) + 1
    provenanceTypes[provenanceType] = (provenanceTypes[provenanceType] || 0) + 1
    reviewStatuses[reviewStatus] = (reviewStatuses[reviewStatus] || 0) + 1
    if (item.source_url_present || item.source_url || item.url) sourceUrlPresent += 1
    else sourceUrlMissing += 1
    if (!analysis?.evidence_review_needed_count && (['low', 'unverified', 'rejected'].includes(trustLabel) || verificationStatus === 'needs_review')) {
      reviewNeeded += 1
    }
    if (!analysis?.evidence_duplicate_item_count && Number(item.duplicate_count || 1) > 1) {
      duplicateItems += Number(item.duplicate_count || 1) - 1
    }
    for (const flag of Array.isArray(item.risk_flags) ? item.risk_flags : []) {
      riskFlags[flag] = (riskFlags[flag] || 0) + 1
    }
    if (item.source_type) itemSources[item.source_type] = (itemSources[item.source_type] || 0) + 1
    if (item.evidence_type) itemTypes[item.evidence_type] = (itemTypes[item.evidence_type] || 0) + 1
  }
  return {
    acquisitionModes,
    count: Number(analysis?.evidence_item_count || currentCase?.evidence_item_count || items.length || 0),
    comments: comments.slice(0, 3),
    duplicateItems,
    provenanceTypes: Object.keys(analysis?.evidence_provenance_type_distribution || {}).length
      ? analysis.evidence_provenance_type_distribution
      : provenanceTypes,
    reviewExcluded: Number(analysis?.evidence_review_excluded_count || 0),
    reviewNeeded,
    reviewStatuses,
    riskFlags,
    sourceDistribution: Object.keys(analysisSources).length ? analysisSources : itemSources,
    sourceUrlMissing,
    sourceUrlPresent,
    titles: titles.slice(0, 4),
    trustLabels: Object.keys(analysis?.evidence_trust_label_distribution || {}).length
      ? analysis.evidence_trust_label_distribution
      : trustLabels,
    typeCounts: Object.keys(analysisTypes).length ? analysisTypes : itemTypes,
    verificationStatuses: Object.keys(analysis?.evidence_verification_status_distribution || {}).length
      ? analysis.evidence_verification_status_distribution
      : verificationStatuses,
  }
}

function DistributionTags({ color = 'blue', values = {} }) {
  const entries = Object.entries(values)
  if (!entries.length) return <Text type="secondary">none</Text>
  return (
    <Space size={[4, 4]} wrap>
      {entries.map(([key, value]) => (
        <Tag color={color} key={key}>
          {key}: {value}
        </Tag>
      ))}
    </Space>
  )
}

export function AnalysisResult({ analysis, currentCase, error, loading, recommendation, summary, visualization }) {
  const { message } = AntApp.useApp()
  const report = useMemo(
    () => buildPublicOpinionReportModel({ analysis, recommendation, summary, visualization }),
    [analysis, recommendation, summary, visualization],
  )
  const sentiment = analysis?.sentiment
  const riskScore = Number(report.overallRisk ?? report.riskScore ?? 0)
  const riskLevel = report.riskLevel
  const topics = analysis?.topics || []
  const botAccounts = analysis?.bot_accounts || []
  const conflicts = analysis?.conflicts || []
  const hasReport = hasReportContent(report)
  const sourceStatus = getAnalysisSourceStatus({ analysis, currentCase })
  const evidenceSummary = useMemo(
    () => buildEvidenceSummary({ analysis, currentCase }),
    [analysis, currentCase],
  )

  const copyResponse = async () => {
    try {
      const copied = await copyTextToClipboard(report.suggestedPublicResponse)
      if (copied) {
        message.success('建议公开回应文案已复制')
        return
      }
    } catch {
      message.error('暂时无法复制建议公开回应文案')
      return
    }
    message.warning('暂无可复制的建议公开回应文案')
  }

  if (!analysis) {
    return (
      <Card className="panel-card">
        {error ? <Alert message="分析结果加载失败" description={error} type="error" showIcon /> : null}
        <Alert
          message="基础分析风险 / Base analysis risk"
          description="Analysis Result 的风险来自当前分析结果；不会自动等同于 Risk Monitor 的最新监控风险或预测风险。analysis_input_source 会标明分析来自 case_raw_data、case_evidence_items 或 mock_data_fallback。"
          showIcon
          type="info"
          style={{ marginBottom: 16 }}
        />
        {loading ? (
          <Skeleton active paragraph={{ rows: 6 }} title />
        ) : (
          <Empty description="暂无分析结果" image={Empty.PRESENTED_IMAGE_SIMPLE} />
        )}
      </Card>
    )
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>分析结果</Title>
          <Text>{analysis.summary || sourceStatus.analysisDescription}</Text>
          <Space wrap className="report-source-strip">
            <Tag color={sourceStatus.dataTagColor}>{sourceStatus.dataLabel}</Tag>
            <Tag color="green">{sourceStatus.analysisLabel}</Tag>
            <Tag color="purple">{sourceStatus.llmLabel}</Tag>
            <Tag color="geekblue">{sourceStatus.sourceDetail}</Tag>
            {sourceStatus.isYoutubeRealData ? <Tag color="red">YouTube public video/comment data</Tag> : null}
          </Space>
        </div>
        <div className={`risk-score-lockup risk-${riskLevel}`}>
          <span>{scoreText(riskScore)}</span>
          <Tag color={riskTone(riskLevel)}>{report.riskLevelLabel}</Tag>
        </div>
      </div>

      <Alert
        message="基础分析风险 / Base analysis risk"
        description={
          <Space direction="vertical" size={2}>
            <Text>该风险来自当前 Analysis Result，不会自动等同于 Risk Monitor 的最新监控风险或预测风险。</Text>
            <Text>analysis_input_source 表示本次分析来自 case_raw_data、case_evidence_items 或 mock_data_fallback；当前计算仍为离线 deterministic pipeline。</Text>
          </Space>
        }
        showIcon
        type="info"
      />

      <Row gutter={[16, 16]}>
        {evidenceSummary.count ? (
          <Col span={24}>
            <Card className="panel-card">
              <Space direction="vertical" className="full-width" size={10}>
                <Space className="report-section-title">
                  <MessageSquareText size={17} />
                  <Title level={4}>Evidence Ingestion</Title>
                </Space>
                <Text type="secondary">
                  Normalized event evidence provides source distribution, evidence type counts, acquisition mode labels, and representative public text for offline analysis. Attachment does not fetch external sources or expose credentials.
                </Text>
                <Space size={[8, 8]} wrap>
                  <Tag color="cyan">evidence_items: {evidenceSummary.count}</Tag>
                  <DistributionTags color="geekblue" values={evidenceSummary.sourceDistribution} />
                  <DistributionTags color="purple" values={evidenceSummary.typeCounts} />
                  <DistributionTags color="gold" values={evidenceSummary.acquisitionModes} />
                  <DistributionTags color="magenta" values={evidenceSummary.provenanceTypes} />
                  <DistributionTags color="lime" values={evidenceSummary.trustLabels} />
                  <DistributionTags color="blue" values={evidenceSummary.verificationStatuses} />
                  <DistributionTags color="volcano" values={evidenceSummary.reviewStatuses} />
                  <Tag color={evidenceSummary.sourceUrlMissing ? 'orange' : 'green'}>
                    source_url_present: {evidenceSummary.sourceUrlPresent}/{evidenceSummary.count}
                  </Tag>
                  <Tag color={evidenceSummary.reviewNeeded ? 'orange' : 'green'}>review_needed: {evidenceSummary.reviewNeeded}</Tag>
                  <Tag color={evidenceSummary.riskFlags?.user_attestation_missing ? 'orange' : 'green'}>
                    attestation_missing: {evidenceSummary.riskFlags?.user_attestation_missing || 0}
                  </Tag>
                  <Tag color={evidenceSummary.duplicateItems ? 'orange' : 'default'}>duplicates collapsed: {evidenceSummary.duplicateItems}</Tag>
                  {evidenceSummary.reviewExcluded ? <Tag color="red">rejected excluded: {evidenceSummary.reviewExcluded}</Tag> : null}
                </Space>
                {Object.keys(evidenceSummary.riskFlags).length ? (
                  <Space size={[4, 4]} wrap>
                    <Text type="secondary">Review flags:</Text>
                    <DistributionTags color="orange" values={evidenceSummary.riskFlags} />
                  </Space>
                ) : null}
                {evidenceSummary.reviewNeeded ? (
                  <Alert
                    message="部分证据来自用户上传或手动录入，需结合来源和人工复核判断。"
                    showIcon
                    type="warning"
                  />
                ) : null}
                {evidenceSummary.reviewExcluded ? (
                  <Alert
                    message="Rejected evidence was excluded from this deterministic analysis by default."
                    showIcon
                    type="info"
                  />
                ) : null}
                {evidenceSummary.titles.length ? (
                  <Text>Top titles: {evidenceSummary.titles.join(' / ')}</Text>
                ) : null}
                {evidenceSummary.comments.length ? (
                  <Text type="secondary">Representative evidence: {evidenceSummary.comments[0]}</Text>
                ) : null}
              </Space>
            </Card>
          </Col>
        ) : null}
        <Col span={8}>
          <Card className="panel-card risk-readout-card">
            <Space className="metric-heading">
              <AlertTriangle size={20} />
              <Text>基础分析风险 / Base analysis risk</Text>
            </Space>
            <Title level={1}>{scoreText(riskScore)}</Title>
            <Space wrap>
              <Tag color={riskTone(riskLevel)}>{report.riskLevelLabel}</Tag>
              <Tag>{riskLevel}</Tag>
              {report.riskModelVersion ? <Tag color="blue">{report.riskModelVersion}</Tag> : null}
            </Space>
            <Paragraph>
              Risk is generated by V1.5 topic risk, sentiment, propagation, controversy, and repeated-script signals.{' '}
              {sourceStatus.isCaseEvidence
                ? 'This run uses offline deterministic analysis from normalized case evidence. Normalized event evidence attached to the case.'
                : sourceStatus.isCaseRawData
                  ? `This run uses offline deterministic analysis from attached case raw data. ${sourceStatus.dataDescription}`
                : 'This run uses the deterministic mock-data fallback.'}
            </Paragraph>
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card">
            <Title level={4}>情绪结构</Title>
            <Space direction="vertical" className="full-width" size={14}>
              <SentimentBar color="#54f5a8" label="正向" value={sentiment?.positive_ratio || 0} />
              <SentimentBar color="#f5c44b" label="中性" value={sentiment?.neutral_ratio || 0} />
              <SentimentBar color="#ff5d8f" label="负向" value={sentiment?.negative_ratio || 0} />
              <Text>平均情绪分：{scoreText(sentiment?.average_sentiment_score || 0)}</Text>
            </Space>
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card">
            <Title level={4}>疑似水军/重复话术影响</Title>
            <Space direction="vertical" className="full-width" size={14}>
              <Space className="analysis-signal-line">
                <Bot size={18} />
                <Text>疑似账号比例</Text>
                <Tag color="cyan">{formatPercent(analysis.bot_score?.suspected_bot_ratio)}</Tag>
              </Space>
              <Space className="analysis-signal-line">
                <MessageCircleWarning size={18} />
                <Text>疑似评论占比</Text>
                <Tag color="volcano">{formatPercent(analysis.bot_score?.suspected_bot_comment_ratio)}</Tag>
              </Space>
              <Text>该指标仅用于舆情研判，不用于身份判断。</Text>
            </Space>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={14}>
          <Card className="panel-card analysis-report-card">
            <div className="panel-heading">
              <Space>
                <FileText size={18} />
                <Title level={4}>报告洞察</Title>
              </Space>
              <Space wrap>
                <Tag color={summary ? 'cyan' : 'default'}>summary/generate</Tag>
                <Tag color={recommendation ? 'green' : 'default'}>recommendation/generate</Tag>
                <Tag color="geekblue">{report.riskModelVersion}</Tag>
              </Space>
            </div>
            {hasReport ? (
              <Space direction="vertical" className="full-width" size={14}>
                <Paragraph className="analysis-report-summary">{report.overallSummary}</Paragraph>
                <Row gutter={[12, 12]}>
                  <Col span={12}>
                    <Space className="report-section-title">
                      <Lightbulb size={16} />
                      <Text strong>核心发现</Text>
                    </Space>
                    <InsightList emptyText="暂无核心发现" items={report.keyFindings.slice(0, 4)} />
                  </Col>
                  <Col span={12}>
                    <Space className="report-section-title">
                      <ShieldAlert size={16} />
                      <Text strong>高风险话题</Text>
                    </Space>
                    <div className="topic-chip-list">
                      {report.topRiskTopics.length ? (
                        report.topRiskTopics.slice(0, 4).map((topic) => (
                          <Tag color={riskTone(topic.riskLevel)} key={topic.topicId}>
                            {topic.topic} · {scoreText(topic.riskScore)}
                          </Tag>
                        ))
                      ) : (
                        <Text type="secondary">报告中暂无高风险话题。</Text>
                      )}
                    </div>
                  </Col>
                </Row>
              </Space>
            ) : (
              <Empty description="暂无报告洞察" image={Empty.PRESENTED_IMAGE_SIMPLE} />
            )}
          </Card>
        </Col>
        <Col span={10}>
          <Card className="panel-card response-template-section">
            <Space className="response-heading">
              <Space className="report-section-title">
                <Target size={17} />
                <Title level={4}>建议公开回应文案</Title>
              </Space>
              <Button
                data-testid="analysis-copy-response-button"
                disabled={!report.suggestedPublicResponse}
                icon={<ClipboardCopy size={16} />}
                onClick={copyResponse}
              >
                复制
              </Button>
            </Space>
            <Paragraph className="response-draft compact-response-draft">
              {report.suggestedPublicResponse || 'recommendation API 暂未返回建议公开回应文案。'}
            </Paragraph>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={8}>
          <Card className="panel-card insight-card">
            <Space className="report-section-title">
              <AlertTriangle size={17} />
              <Title level={4}>情绪解释</Title>
            </Space>
            <Paragraph>{report.sentimentExplanation}</Paragraph>
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card insight-card">
            <Space className="report-section-title">
              <Bot size={17} />
              <Title level={4}>疑似水军/重复话术解释</Title>
            </Space>
            <Paragraph>{report.botSignalExplanation}</Paragraph>
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card insight-card">
            <Space className="report-section-title">
              <MessageSquareText size={17} />
              <Title level={4}>代表性评论</Title>
            </Space>
            <InsightList emptyText="暂无代表性评论" items={report.representativeComments.slice(0, 4)} />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={14}>
          <SentimentTrendChart data={visualization?.sentiment_trend || []} focusNegative />
        </Col>
        <Col span={10}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Space>
                <ShieldAlert size={18} />
                <Title level={4}>V1.5 话题风险卡片</Title>
              </Space>
              <Tag color="geekblue">{report.riskModelVersion}</Tag>
            </div>
            <TopicRiskCards items={report.topicRisks} />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={14}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Title level={4}>话题聚类</Title>
              <Tag color="cyan">{topics.length}</Tag>
            </div>
            <Table columns={topicColumns} dataSource={topics} pagination={false} rowKey="cluster_id" size="middle" />
          </Card>
        </Col>
        <Col span={10}>
          <Card className="panel-card">
            <Title level={4}>账号与争议信号</Title>
            <List
              dataSource={botAccounts}
              locale={{ emptyText: 'mock 结果中暂无疑似账号' }}
              renderItem={(item) => (
                <List.Item>
                  <List.Item.Meta
                    title={
                      <Space wrap>
                        <Text>{item.author_id}</Text>
                        <Tag color="volcano">{formatPercent(item.bot_probability)}</Tag>
                      </Space>
                    }
                    description={(item.bot_reasons || []).join(' / ') || '暂无原因'}
                  />
                </List.Item>
              )}
            />
            <List
              dataSource={conflicts}
              locale={{ emptyText: '暂无争议信号' }}
              renderItem={(item) => (
                <List.Item>
                  <List.Item.Meta
                    title={<Tag color="red">争议强度 {formatPercent(item.intensity)}</Tag>}
                    description={
                      <div className="conflict-copy">
                        <Paragraph>{item.side_a}</Paragraph>
                        <Paragraph>{item.side_b}</Paragraph>
                      </div>
                    }
                  />
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>
    </div>
  )
}
