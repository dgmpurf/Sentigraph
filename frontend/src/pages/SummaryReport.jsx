import { Button, Card, Col, List, Row, Space, Typography } from 'antd'
import { ClipboardCopy } from 'lucide-react'

const { Paragraph, Text, Title } = Typography

export function SummaryReport({ recommendation, summary }) {
  const responseText = recommendation?.suggested_response || ''
  const copyResponse = () => {
    if (responseText) navigator.clipboard?.writeText(responseText)
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>Summary Report</Title>
          <Text>Mock executive summary, risks, response actions, and draft statement.</Text>
        </div>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card className="panel-card report-panel">
            <Title level={4}>Executive Summary</Title>
            <Paragraph>{summary?.summary || 'No summary loaded.'}</Paragraph>
            <Title level={4}>Key Findings</Title>
            <List
              dataSource={summary?.key_findings || []}
              renderItem={(item) => (
                <List.Item>
                  <Text>{item}</Text>
                </List.Item>
              )}
            />
            <Title level={4}>Representative Comments</Title>
            <List
              dataSource={summary?.representative_comments || []}
              renderItem={(item) => (
                <List.Item>
                  <Text>{item}</Text>
                </List.Item>
              )}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card className="panel-card report-panel">
            <Title level={4}>Recommended Actions</Title>
            <List
              dataSource={recommendation?.recommended_actions || []}
              renderItem={(item) => (
                <List.Item>
                  <Text>{item}</Text>
                </List.Item>
              )}
            />
            <Title level={4}>Main Risks</Title>
            <List
              dataSource={recommendation?.main_risks || []}
              renderItem={(item) => (
                <List.Item>
                  <Text>{item}</Text>
                </List.Item>
              )}
            />
            <Space className="response-heading">
              <Title level={4}>Suggested Response</Title>
              <Button icon={<ClipboardCopy size={16} />} onClick={copyResponse}>
                Copy
              </Button>
            </Space>
            <Paragraph className="response-draft">{responseText}</Paragraph>
          </Card>
        </Col>
      </Row>
    </div>
  )
}
