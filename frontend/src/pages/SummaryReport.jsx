import { Alert, App as AntApp, Button, Card, Col, Empty, Row, Skeleton, Space, Statistic, Tag, Typography } from 'antd'
import { Bot, ClipboardCopy, Download, FileText, ShieldAlert, Siren, Target } from 'lucide-react'

import { PublicOpinionReport } from '../components/report/PublicOpinionReport.jsx'
import { copyTextToClipboard } from '../utils/clipboard.js'
import { formatPercent, riskTone } from '../utils/formatters.js'
import { buildPublicOpinionReportModel, hasReportContent } from '../utils/reportModel.js'

const { Text, Title } = Typography

function scoreText(value) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue.toFixed(1) : '0.0'
}

export function SummaryReport({
  analysis,
  currentCase,
  error,
  loading,
  markdownLoading,
  markdownReport,
  onGetMarkdownReport,
  recommendation,
  summary,
  visualization,
}) {
  const { message } = AntApp.useApp()
  const report = buildPublicOpinionReportModel({ analysis, recommendation, summary, visualization })
  const hasBackendReportData = Boolean(summary || recommendation)
  const hasContent = hasReportContent(report) && hasBackendReportData
  const negativeRatio = analysis?.sentiment?.negative_ratio ?? visualization?.risk_radar?.negative_sentiment ?? 0
  const botImpact =
    visualization?.bot_impact?.suspected_bot_comment_ratio ??
    analysis?.bot_score?.suspected_bot_comment_ratio ??
    0
  const overallRisk = report.overallRisk ?? report.riskScore ?? 0

  const copyMarkdown = async () => {
    try {
      const exportData = markdownReport || (await onGetMarkdownReport?.())
      const copied = await copyTextToClipboard(exportData?.markdown || '')
      if (copied) {
        message.success('Markdown 报告已复制')
        return
      }
      message.warning('暂无可复制的 Markdown 报告')
    } catch (copyError) {
      message.error(copyError?.message || '暂时无法复制 Markdown 报告')
    }
  }

  const downloadMarkdown = async () => {
    try {
      const exportData = markdownReport || (await onGetMarkdownReport?.())
      if (!exportData?.markdown) {
        message.warning('暂无可下载的 Markdown 报告')
        return
      }
      const blob = new Blob([exportData.markdown], { type: 'text/markdown;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = exportData.filename || 'sentigraph_report.md'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
      message.success('Markdown 报告已生成')
    } catch (downloadError) {
      message.error(downloadError?.message || '暂时无法下载 Markdown 报告')
    }
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>舆情报告</Title>
          <Text>来自后端离线 mock 管线和模板报告生成器的结构化中文报告。</Text>
          <Space wrap className="report-source-strip">
            <Tag color={summary ? 'cyan' : 'default'}>summary API {summary ? '已加载' : '暂无数据'}</Tag>
            <Tag color={recommendation ? 'green' : 'default'}>
              recommendation API {recommendation ? '已加载' : '暂无数据'}
            </Tag>
            <Tag color="geekblue">{report.reportLanguage}</Tag>
            {report.riskModelVersion ? <Tag color="blue">{report.riskModelVersion}</Tag> : null}
            {currentCase?.case_id ? <Tag color="purple">{currentCase.case_id}</Tag> : null}
          </Space>
        </div>
        <Space align="end" direction="vertical" size={8}>
          <Tag color={riskTone(report.riskLevel)} className="large-tag">
            {report.riskLevelLabel}
          </Tag>
          <Space>
            <Button
              disabled={!currentCase?.case_id || !hasContent}
              icon={<ClipboardCopy size={16} />}
              loading={markdownLoading}
              onClick={copyMarkdown}
            >
              复制 Markdown
            </Button>
            <Button
              disabled={!currentCase?.case_id || !hasContent}
              icon={<Download size={16} />}
              loading={markdownLoading}
              onClick={downloadMarkdown}
              type="primary"
            >
              下载 .md
            </Button>
          </Space>
        </Space>
      </div>

      {error ? <Alert message="报告数据加载失败" description={error} type="error" showIcon /> : null}

      <Row gutter={[16, 16]}>
        <Col span={6}>
          <Card className={`metric-card risk-level-card risk-${report.riskLevel}`}>
            <ShieldAlert size={20} />
            <Statistic title="风险分数" value={scoreText(overallRisk)} suffix="/100" />
            <Tag color={riskTone(report.riskLevel)}>{report.riskLevelLabel}</Tag>
            <Text type="secondary">{report.riskLevel}</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Siren size={20} />
            <Statistic title="负面情绪" value={formatPercent(negativeRatio)} />
            <Text>情绪趋势主信号</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Target size={20} />
            <Statistic title="V1.5 高风险话题" value={report.topRiskTopics.length || report.topNegativeTopics.length} />
            <Text>报告识别的话题级风险</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Bot size={20} />
            <Statistic title="操纵/重复话术风险" value={scoreText(report.manipulationRisk ?? botImpact * 100)} suffix="/100" />
            <Text>重复话术/协同信号</Text>
          </Card>
        </Col>
      </Row>

      {loading && !hasContent ? (
        <Card className="panel-card report-export-section">
          <Skeleton active paragraph={{ rows: 8 }} title />
        </Card>
      ) : hasContent ? (
        <PublicOpinionReport report={report} />
      ) : (
        <Card className="panel-card">
          <Empty
            description="后端报告 API 暂无 summary 或 recommendation 数据"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          />
        </Card>
      )}
    </div>
  )
}
