import { Button, Card, DatePicker, Form, Input, InputNumber, Select, Space, Tag, Typography } from 'antd'
import { Search } from 'lucide-react'

const { RangePicker } = DatePicker
const { Text, Title } = Typography

const DEFAULT_PLATFORM_OPTIONS = [
  { label: 'Reddit', value: 'reddit' },
  { label: 'Weibo', value: 'weibo' },
]

const PLATFORM_GROUPS = [
  {
    key: 'mock_selectable',
    title: 'MVP mock-selectable platforms',
    description: 'Enabled for offline mock analysis only. These selections do not call real platform APIs.',
    color: 'cyan',
    filter: (platform) => platform.selectable_for_mock,
  },
  {
    key: 'official_api_planned',
    title: 'Official API planned platforms',
    description: 'Visible in the roadmap and selectable only for mock analysis until credentials are available.',
    color: 'blue',
    filter: (platform) => platform.category === 'official_api_planned',
  },
  {
    key: 'future_real_adapter_candidate',
    title: 'Future real adapter candidates',
    description: 'Potential future real adapters after compliance and API design review.',
    color: 'geekblue',
    filter: (platform) => platform.category === 'future_real_adapter_candidate',
  },
  {
    key: 'crawler_later',
    title: 'Crawler-later platforms',
    description: 'Future crawler integration',
    color: 'gold',
    filter: (platform) => platform.category === 'crawler_later',
  },
  {
    key: 'disabled_or_optional_future',
    title: 'Disabled or optional future platforms',
    description: 'Not active in the current MVP roadmap.',
    color: 'default',
    filter: (platform) => platform.category === 'disabled_or_optional_future',
  },
]

function getPlatformGroups(platformRegistry) {
  return PLATFORM_GROUPS.map((group) => ({
    ...group,
    platforms: platformRegistry.filter(group.filter),
  }))
}

function PlatformRoadmap({ platformRegistry }) {
  if (!platformRegistry?.length) {
    return (
      <Card className="panel-card">
        <div className="panel-heading">
          <Title level={4}>Platform Roadmap</Title>
          <Text type="secondary">Backend platform registry is unavailable. Mock fallback choices are shown.</Text>
        </div>
      </Card>
    )
  }

  return (
    <Card className="panel-card">
      <div className="panel-heading">
        <div>
          <Title level={4}>Platform Roadmap</Title>
          <Text type="secondary">Selection is mock-first. No real crawler or third-party API call is triggered.</Text>
        </div>
      </div>
      <div className="platform-roadmap-grid">
        {getPlatformGroups(platformRegistry).map((group) => (
          <div className="platform-group" key={group.key}>
            <div className="platform-group-header">
              <Text strong>{group.title}</Text>
              <Text type="secondary">{group.description}</Text>
            </div>
            <div className="platform-list">
              {group.platforms.length ? (
                group.platforms.map((platform) => (
                  <div className="platform-item" key={`${group.key}-${platform.platform_id}`}>
                    <Space size={6} wrap>
                      <Tag color={group.color}>{platform.display_name}</Tag>
                      {platform.selectable_for_mock ? <Tag color="green">Mock selectable</Tag> : <Tag>Disabled</Tag>}
                    </Space>
                    <Text className="platform-note" type="secondary">
                      {platform.notes}
                    </Text>
                  </div>
                ))
              ) : (
                <Text type="secondary">No platforms in this group.</Text>
              )}
            </div>
          </div>
        ))}
      </div>
    </Card>
  )
}

function normalizeDateRange(dateRange) {
  if (!dateRange?.length) return { start: '2026-05-01', end: '2026-05-13' }
  return {
    start: dateRange[0].format('YYYY-MM-DD'),
    end: dateRange[1].format('YYYY-MM-DD'),
  }
}

export function KeywordSearch({
  expandedKeywords,
  initialPlatforms = ['reddit', 'weibo'],
  loading,
  onStartAnalysis,
  platformOptions = DEFAULT_PLATFORM_OPTIONS,
  platformRegistry = [],
}) {
  const selectOptions = [{ label: 'MVP mock-selectable platforms', options: platformOptions }]

  const handleFinish = (values) => {
    onStartAnalysis({
      title: values.title,
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
          initialValues={{ keyword: 'Tesla', platforms: initialPlatforms, language: 'auto', limit: 100 }}
          onFinish={handleFinish}
        >
          <div className="form-grid">
            <Form.Item label="Case Title" name="title">
              <Input size="large" placeholder="Optional, for example Tesla product risk watch" />
            </Form.Item>
            <Form.Item
              label="Keyword"
              name="keyword"
              rules={[{ required: true, message: 'Enter one keyword to analyze.' }]}
            >
              <Input size="large" placeholder="Tesla, product name, public figure..." />
            </Form.Item>
            <Form.Item label="Platforms" name="platforms" rules={[{ required: true }]}>
              <Select
                mode="multiple"
                size="large"
                options={selectOptions}
                placeholder="Select mock-enabled MVP platforms"
              />
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
            Create Case & Run Mock Analysis
          </Button>
        </Form>
      </Card>

      <PlatformRoadmap platformRegistry={platformRegistry} />

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
