import { Button, Card, DatePicker, Form, Input, InputNumber, Select, Space, Tag, Typography } from 'antd'
import { Search } from 'lucide-react'

const { RangePicker } = DatePicker
const { Text, Title } = Typography

const platformOptions = [
  { label: 'Reddit', value: 'reddit' },
  { label: 'Weibo', value: 'weibo' },
  { label: 'YouTube', value: 'youtube' },
  { label: 'Bilibili', value: 'bilibili' },
]

function normalizeDateRange(dateRange) {
  if (!dateRange?.length) return { start: '2026-05-01', end: '2026-05-13' }
  return {
    start: dateRange[0].format('YYYY-MM-DD'),
    end: dateRange[1].format('YYYY-MM-DD'),
  }
}

export function KeywordSearch({ expandedKeywords, loading, onStartAnalysis }) {
  const handleFinish = (values) => {
    onStartAnalysis({
      keyword: values.keyword,
      platforms: values.platforms,
      language: values.language,
      limit: values.limit,
      date_range: normalizeDateRange(values.date_range),
    })
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>Keyword Search</Title>
          <Text>Start a mock monitoring project with selected public platforms.</Text>
        </div>
      </div>

      <Card className="panel-card form-panel">
        <Form
          layout="vertical"
          initialValues={{ keyword: 'Tesla', platforms: ['reddit', 'weibo'], language: 'auto', limit: 100 }}
          onFinish={handleFinish}
        >
          <div className="form-grid">
            <Form.Item
              label="Keyword"
              name="keyword"
              rules={[{ required: true, message: 'Enter one keyword to analyze.' }]}
            >
              <Input size="large" placeholder="Tesla, product name, public figure..." />
            </Form.Item>
            <Form.Item label="Platforms" name="platforms" rules={[{ required: true }]}>
              <Select mode="multiple" size="large" options={platformOptions} />
            </Form.Item>
            <Form.Item label="Date Range" name="date_range">
              <RangePicker size="large" className="full-width" />
            </Form.Item>
            <Form.Item label="Limit" name="limit">
              <InputNumber size="large" min={10} max={1000} step={10} className="full-width" />
            </Form.Item>
            <Form.Item label="Language" name="language">
              <Select
                size="large"
                options={[
                  { label: 'Auto', value: 'auto' },
                  { label: 'English', value: 'en' },
                  { label: 'Chinese', value: 'zh' },
                ]}
              />
            </Form.Item>
          </div>
          <Button type="primary" htmlType="submit" icon={<Search size={17} />} loading={loading} size="large">
            Start Mock Analysis
          </Button>
        </Form>
      </Card>

      {expandedKeywords ? (
        <Card className="panel-card">
          <div className="panel-heading">
            <Title level={4}>Expanded Keywords</Title>
            <Text>{expandedKeywords.original_keyword}</Text>
          </div>
          <Space wrap>
            {expandedKeywords.expanded_keywords.map((keyword) => (
              <Tag color="cyan" key={keyword}>
                {keyword}
              </Tag>
            ))}
          </Space>
          <div className="query-strip">
            {expandedKeywords.search_queries.map((query) => (
              <Text code key={query}>
                {query}
              </Text>
            ))}
          </div>
        </Card>
      ) : null}
    </div>
  )
}

