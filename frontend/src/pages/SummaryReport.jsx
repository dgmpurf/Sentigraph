import { Card, Col, Empty, Row, Statistic, Tag, Typography } from 'antd'
import { FileDown, ShieldAlert, Siren, Target } from 'lucide-react'

import { PublicOpinionReport } from '../components/report/PublicOpinionReport.jsx'
import { buildPublicOpinionReportModel } from '../utils/reportModel.js'
import { formatPercent, riskTone } from '../utils/formatters.js'

const { Text, Title } = Typography

export function SummaryReport({ analysis, recommendation, summary, visualization }) {
  const report = buildPublicOpinionReportModel({ analysis, recommendation, summary, visualization })
  const negativeRatio = analysis?.sentiment?.negative_ratio ?? visualization?.risk_radar?.negative_sentiment ?? 0
  const botImpact = visualization?.bot_impact?.suspected_bot_comment_ratio ?? analysis?.bot_score?.suspected_bot_comment_ratio ?? 0

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>Summary Report</Title>
          <Text>Export-friendly public opinion briefing from the offline mock pipeline.</Text>
        </div>
        <Tag color={riskTone(report.riskLevel)} className="large-tag">
          {report.riskLevel} risk
        </Tag>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={6}>
          <Card className={`metric-card risk-level-card risk-${report.riskLevel}`}>
            <ShieldAlert size={20} />
            <Statistic title="Risk Score" value={report.riskScore} suffix="/100" />
            <Tag color={riskTone(report.riskLevel)}>{report.riskLevel}</Tag>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Siren size={20} />
            <Statistic title="Negative Sentiment" value={formatPercent(negativeRatio)} />
            <Text>Primary trend signal</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Target size={20} />
            <Statistic title="Negative Topics" value={report.topNegativeTopics.length} />
            <Text>Topic groups in report</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <FileDown size={20} />
            <Statistic title="Bot Impact" value={formatPercent(botImpact)} />
            <Text>PDF export planned later</Text>
          </Card>
        </Col>
      </Row>

      {summary || recommendation ? (
        <PublicOpinionReport report={report} />
      ) : (
        <Card className="panel-card">
          <Empty description="No summary or recommendation data loaded" image={Empty.PRESENTED_IMAGE_SIMPLE} />
        </Card>
      )}
    </div>
  )
}
