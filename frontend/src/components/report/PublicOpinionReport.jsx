import { Button, Card, Col, Empty, List, Row, Space, Tag, Typography } from 'antd'
import {
  AlertTriangle,
  Bot,
  ClipboardCopy,
  FileText,
  MessageSquareText,
  ShieldCheck,
  Target,
} from 'lucide-react'

import { hasReportContent } from '../../utils/reportModel.js'
import { riskTone } from '../../utils/formatters.js'

const { Paragraph, Text, Title } = Typography

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

export function PublicOpinionReport({ report }) {
  const copyResponse = () => {
    if (report?.suggestedPublicResponse) navigator.clipboard?.writeText(report.suggestedPublicResponse)
  }

  if (!hasReportContent(report)) {
    return (
      <Card className="panel-card report-export-section">
        <Empty description="No public opinion report loaded" image={Empty.PRESENTED_IMAGE_SIMPLE} />
      </Card>
    )
  }

  return (
    <Card className="panel-card report-export-section">
      <div className="report-header">
        <div>
          <Space size={10} className="section-kicker">
            <FileText size={17} />
            <Text>Export-ready briefing</Text>
          </Space>
          <Title level={3}>Public Opinion Report</Title>
          <Paragraph>{report.overallSummary}</Paragraph>
        </div>
        <div className={`report-risk-badge risk-${report.riskLevel}`}>
          <span>{report.riskScore}</span>
          <Tag color={riskTone(report.riskLevel)}>{report.riskLevel} risk</Tag>
        </div>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <section className="report-section">
            <Space className="report-section-title">
              <AlertTriangle size={17} />
              <Title level={4}>Main Risk Factors</Title>
            </Space>
            <ReportList emptyText="No major risk factors" items={report.mainRiskFactors} />
          </section>
        </Col>
        <Col span={12}>
          <section className="report-section">
            <Space className="report-section-title">
              <Target size={17} />
              <Title level={4}>Top Negative Topics</Title>
            </Space>
            <ReportList emptyText="No negative topics detected" items={report.topNegativeTopics} />
          </section>
        </Col>
        <Col span={12}>
          <section className="report-section">
            <Space className="report-section-title">
              <MessageSquareText size={17} />
              <Title level={4}>Representative Comments</Title>
            </Space>
            <ReportList emptyText="No representative comments" items={report.representativeComments} />
          </section>
        </Col>
        <Col span={12}>
          <section className="report-section">
            <Space className="report-section-title">
              <Bot size={17} />
              <Title level={4}>Bot and Repeated-Script Signals</Title>
            </Space>
            <ReportList emptyText="No bot-like signal in report" items={report.suspectedBotSignals} />
          </section>
        </Col>
        <Col span={12}>
          <section className="report-section">
            <Space className="report-section-title">
              <ShieldCheck size={17} />
              <Title level={4}>Recommended Response Actions</Title>
            </Space>
            <ReportList emptyText="No recommended actions" items={report.recommendedActions} marker="number" />
          </section>
        </Col>
        <Col span={12}>
          <section className="report-section response-template-section">
            <Space className="response-heading">
              <Space className="report-section-title">
                <FileText size={17} />
                <Title level={4}>Suggested Public Response</Title>
              </Space>
              <Button icon={<ClipboardCopy size={16} />} onClick={copyResponse}>
                Copy
              </Button>
            </Space>
            <Paragraph className="response-draft">{report.suggestedPublicResponse || 'No response template loaded.'}</Paragraph>
          </section>
        </Col>
      </Row>
    </Card>
  )
}
