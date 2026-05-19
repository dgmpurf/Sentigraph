import { App as AntApp, Button, Card, Col, Empty, List, Progress, Row, Space, Tag, Typography } from 'antd'
import {
  AlertTriangle,
  Bot,
  ClipboardCopy,
  FileText,
  Lightbulb,
  MessageSquareText,
  ShieldAlert,
  ShieldCheck,
  Target,
} from 'lucide-react'

import { copyTextToClipboard } from '../../utils/clipboard.js'
import { formatPercent, riskTone } from '../../utils/formatters.js'
import { hasReportContent } from '../../utils/reportModel.js'

const { Paragraph, Text, Title } = Typography

const riskLevelLabels = {
  low: '低风险',
  medium: '中等风险',
  high: '高风险',
  critical: '严重风险',
}

function scoreText(value) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue.toFixed(1) : '0.0'
}

function ReportList({ emptyText, items, marker = 'dot' }) {
  return (
    <List
      className={`report-list report-list-${marker}`}
      dataSource={items}
      locale={{ emptyText }}
      renderItem={(item, index) => (
        <List.Item>
          <Space align="start" size={10}>
            <span className="report-list-marker">{marker === 'number' ? index + 1 : ''}</span>
            <Text>{item}</Text>
          </Space>
        </List.Item>
      )}
    />
  )
}

function TopicRiskReportList({ items }) {
  return (
    <List
      className="report-topic-risk-list"
      dataSource={items}
      locale={{ emptyText: '暂无 V1.5 话题风险数据' }}
      renderItem={(item, index) => {
        const riskScore = Number(item.riskScore || 0)
        return (
          <List.Item>
            <div className={`report-topic-risk-item risk-${item.riskLevel}`}>
              <Space direction="vertical" className="full-width" size={8}>
                <Space className="analysis-signal-line" wrap>
                  <Text strong>{index + 1}. {item.topic}</Text>
                  <Tag color={riskTone(item.riskLevel)}>{riskLevelLabels[item.riskLevel] || item.riskLevel}</Tag>
                  <Tag color="volcano">{scoreText(riskScore)}/100</Tag>
                </Space>
                <Progress percent={Math.round(riskScore)} showInfo={false} strokeColor="#ff5d8f" trailColor="#283043" />
                <div className="topic-risk-meta-grid">
                  <span>评论数：{item.commentCount || 0}</span>
                  <span>负面占比：{formatPercent(item.negativeRatio || 0)}</span>
                  <span>争议信号：{formatPercent(item.controversySignal || 0)}</span>
                  <span>扩散信号：{formatPercent(item.spreadSignal || 0)}</span>
                </div>
                <Text type="secondary">{item.explanation || '暂无风险解释。'}</Text>
              </Space>
            </div>
          </List.Item>
        )
      }}
    />
  )
}

export function PublicOpinionReport({ report }) {
  const { message } = AntApp.useApp()

  const copyResponse = async () => {
    try {
      const copied = await copyTextToClipboard(report?.suggestedPublicResponse || '')
      if (copied) {
        message.success('建议回应文案已复制')
        return
      }
    } catch {
      message.error('暂时无法复制建议回应文案')
      return
    }
    message.warning('暂无可复制的建议回应文案')
  }

  if (!hasReportContent(report)) {
    return (
      <Card className="panel-card report-export-section">
        <Empty description="暂无舆情报告数据" image={Empty.PRESENTED_IMAGE_SIMPLE} />
      </Card>
    )
  }

  const overallRisk = report.overallRisk ?? report.riskScore ?? 0

  return (
    <Card className="panel-card report-export-section">
      <div className="report-header">
        <div>
          <Space size={10} className="section-kicker">
            <FileText size={17} />
            <Text>Public Opinion Report</Text>
          </Space>
          <Title level={3}>结构化中文舆情报告</Title>
          <Space wrap className="report-source-strip">
            <Tag color={report.hasSummaryData ? 'cyan' : 'default'}>summary/generate</Tag>
            <Tag color={report.hasRecommendationData ? 'green' : 'default'}>recommendation/generate</Tag>
            <Tag color={report.generatedFromMockPipeline ? 'purple' : 'cyan'}>
              {report.generatedFromMockPipeline ? 'Mock fallback report' : 'Attached raw-data report'}
            </Tag>
            <Tag color="geekblue">{report.reportLanguage}</Tag>
            {report.riskModelVersion ? <Tag color="blue">{report.riskModelVersion}</Tag> : null}
          </Space>
        </div>
        <div className={`report-risk-badge risk-${report.riskLevel}`}>
          <span>{scoreText(overallRisk)}</span>
          <Tag color={riskTone(report.riskLevel)}>{report.riskLevelLabel}</Tag>
          <Text type="secondary">{report.riskLevel}</Text>
        </div>
      </div>

      <div className="report-meta-grid">
        <div>
          <Text type="secondary">项目ID</Text>
          <Text strong>{report.projectId || 'mock_project'}</Text>
        </div>
        <div>
          <Text type="secondary">报告语言</Text>
          <Text strong>{report.reportLanguage}</Text>
        </div>
        <div>
          <Text type="secondary">风险分数</Text>
          <Text strong>{scoreText(overallRisk)}/100</Text>
        </div>
        <div>
          <Text type="secondary">风险等级</Text>
          <Space size={6}>
            <Tag color={riskTone(report.riskLevel)}>{report.riskLevelLabel}</Tag>
            <Text>{report.riskLevel}</Text>
          </Space>
        </div>
        <div>
          <Text type="secondary">风险模型版本</Text>
          <Text strong>{report.riskModelVersion}</Text>
        </div>
        <div>
          <Text type="secondary">真实危机风险</Text>
          <Text strong>{scoreText(report.realCrisisRisk ?? 0)}/100</Text>
        </div>
        <div>
          <Text type="secondary">操纵/重复话术风险</Text>
          <Text strong>{scoreText(report.manipulationRisk ?? 0)}/100</Text>
        </div>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={24}>
          <section className="report-section report-overview-section">
            <Space className="report-section-title">
              <FileText size={17} />
              <Title level={4}>舆情总览</Title>
            </Space>
            <Paragraph className="report-overview-copy">
              {report.overallSummary || '暂无总览摘要。'}
            </Paragraph>
          </section>
        </Col>
        <Col span={24}>
          <section className="report-section report-topic-risk-section">
            <Space className="report-section-title">
              <ShieldAlert size={17} />
              <Title level={4}>V1.5 高风险话题</Title>
            </Space>
            {report.riskExplanation ? <Paragraph>{report.riskExplanation}</Paragraph> : null}
            <TopicRiskReportList items={report.topRiskTopics} />
          </section>
        </Col>
        <Col span={12}>
          <section className="report-section">
            <Space className="report-section-title">
              <Lightbulb size={17} />
              <Title level={4}>核心发现</Title>
            </Space>
            <ReportList emptyText="暂无核心发现" items={report.keyFindings} />
          </section>
        </Col>
        <Col span={12}>
          <section className="report-section">
            <Space className="report-section-title">
              <AlertTriangle size={17} />
              <Title level={4}>主要风险因素</Title>
            </Space>
            <ReportList emptyText="暂无主要风险因素" items={report.mainRiskFactors} />
          </section>
        </Col>
        <Col span={12}>
          <section className="report-section">
            <Space className="report-section-title">
              <Target size={17} />
              <Title level={4}>负面/高风险议题</Title>
            </Space>
            <ReportList emptyText="暂无负面或高风险议题" items={report.topNegativeTopics} />
          </section>
        </Col>
        <Col span={12}>
          <section className="report-section">
            <Space className="report-section-title">
              <MessageSquareText size={17} />
              <Title level={4}>代表性评论</Title>
            </Space>
            <ReportList emptyText="暂无代表性评论" items={report.representativeComments} />
          </section>
        </Col>
        <Col span={12}>
          <section className="report-section">
            <Space className="report-section-title">
              <Bot size={17} />
              <Title level={4}>疑似水军/重复话术信号</Title>
            </Space>
            <ReportList emptyText="暂无疑似水军或重复话术信号" items={report.suspectedBotSignals} />
          </section>
        </Col>
        <Col span={12}>
          <section className="report-section">
            <Space className="report-section-title">
              <ShieldCheck size={17} />
              <Title level={4}>建议行动</Title>
            </Space>
            <ReportList emptyText="暂无建议行动" items={report.recommendedActions} marker="number" />
          </section>
        </Col>
        <Col span={24}>
          <section className="report-section response-template-section">
            <Space className="response-heading">
              <Space className="report-section-title">
                <FileText size={17} />
                <Title level={4}>建议公开回应文案</Title>
              </Space>
              <Button
                data-testid="summary-copy-response-button"
                disabled={!report.suggestedPublicResponse}
                icon={<ClipboardCopy size={16} />}
                onClick={copyResponse}
                type="primary"
              >
                复制文案
              </Button>
            </Space>
            <Paragraph className="response-draft">
              {report.suggestedPublicResponse || '暂无建议公开回应文案。'}
            </Paragraph>
          </section>
        </Col>
      </Row>
    </Card>
  )
}
