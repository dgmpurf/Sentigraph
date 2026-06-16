import { Alert, Button, Card, Checkbox, Col, Input, Row, Select, Space, Tag, Typography } from 'antd'
import { ArrowLeft, Building2, CheckCircle2, ClipboardList, Info, ShieldCheck, ThumbsUp } from 'lucide-react'
import { useMemo, useState } from 'react'

import { PUBLIC_EVENT_PLAZA_EVENTS } from '../data/publicEventSamples.js'

const { Paragraph, Text, Title } = Typography
const { TextArea } = Input

const EVENT_TYPE_OPTIONS = [
  { label: '游戏 / 社区事件', value: 'game' },
  { label: '动漫 / ACG 事件', value: 'anime' },
  { label: '品牌 / 产品事件', value: 'brand' },
  { label: '创作者 / UP 主事件', value: 'creator' },
  { label: '公共服务 / 社会议题', value: 'community' },
  { label: '其他公开事件', value: 'other' },
]

const FOCUS_OPTIONS = [
  '舆论走向',
  '社区反应',
  '官方回应',
  '长期声誉',
  '证据边界',
  '其他',
]

const INITIAL_FORM = {
  title: '',
  eventType: 'game',
  publicLinks: '',
  platformContext: '',
  reason: '',
  focusAreas: ['舆论走向'],
  attestedMock: false,
}

function SupportCandidateCard({ event, supported, supportCount, onSupport }) {
  return (
    <Card className="panel-card public-request-vote-card">
      <Space direction="vertical" size={10} className="full-width">
        <Space wrap>
          <Tag color="cyan">{event.event_type_label}</Tag>
          <Tag>{event.sample_label}</Tag>
          <Tag color="gold">候选公开样本</Tag>
        </Space>
        <div>
          <Title level={4}>{event.title}</Title>
          <Paragraph>{event.request_note}</Paragraph>
        </div>
        <div className="public-request-count-grid">
          <div>
            <Text type="secondary">本地演示请求数</Text>
            <strong>{event.request_count_mock}</strong>
          </div>
          <div>
            <Text type="secondary">本地演示支持数</Text>
            <strong>{supportCount}</strong>
          </div>
        </div>
        <Button
          icon={supported ? <CheckCircle2 size={16} /> : <ThumbsUp size={16} />}
          disabled={supported}
          onClick={() => onSupport(event.event_id)}
          type={supported ? 'default' : 'primary'}
        >
          {supported ? '已支持（仅本地演示）' : '支持我们优先做这个公开样本'}
        </Button>
        <Text type="secondary">
          支持数只用于本地 demo 展示，不代表自然舆情热度、真实公众需求或真实排序。
        </Text>
      </Space>
    </Card>
  )
}

function TrackCard({ icon, title, description, tags, primary }) {
  return (
    <Card className={`panel-card public-request-track-card ${primary ? 'primary-track' : ''}`}>
      <Space direction="vertical" size={12} className="full-width">
        <div className="public-request-track-icon">{icon}</div>
        <div>
          <Title level={4}>{title}</Title>
          <Paragraph>{description}</Paragraph>
        </div>
        <Space wrap>
          {tags.map((tag) => (
            <Tag key={tag} color={primary ? 'cyan' : 'purple'}>
              {tag}
            </Tag>
          ))}
        </Space>
      </Space>
    </Card>
  )
}

export function PublicEventRequest() {
  const supportCandidates = useMemo(
    () => PUBLIC_EVENT_PLAZA_EVENTS.filter((event) => !event.is_sample_available).slice(0, 4),
    [],
  )
  const initialSupportCounts = useMemo(
    () => Object.fromEntries(supportCandidates.map((event) => [event.event_id, event.vote_count_mock])),
    [supportCandidates],
  )
  const [formValues, setFormValues] = useState(INITIAL_FORM)
  const [validationMessage, setValidationMessage] = useState('')
  const [preview, setPreview] = useState(null)
  const [supportedEventIds, setSupportedEventIds] = useState([])
  const [supportCounts, setSupportCounts] = useState(initialSupportCounts)
  const [localNote, setLocalNote] = useState('')
  const [showBEndPanel, setShowBEndPanel] = useState(false)

  const goToHash = (hash) => {
    window.location.hash = hash
  }

  const updateForm = (field, value) => {
    setFormValues((current) => ({ ...current, [field]: value }))
  }

  const submitPreview = () => {
    if (!formValues.title.trim() || !formValues.reason.trim() || !formValues.attestedMock) {
      setValidationMessage('请填写事件名称、请求理由，并确认这是不会真实提交的本地演示入口。')
      setPreview(null)
      return
    }

    setValidationMessage('')
    setPreview({
      title: formValues.title.trim(),
      eventType: EVENT_TYPE_OPTIONS.find((option) => option.value === formValues.eventType)?.label || formValues.eventType,
      publicLinks: formValues.publicLinks.trim() || '未填写公开线索 URL',
      platformContext: formValues.platformContext.trim() || '未填写平台 / 场景',
      reason: formValues.reason.trim(),
      focusAreas: formValues.focusAreas.length ? formValues.focusAreas : ['未选择重点'],
    })
    setLocalNote('已生成本地演示预览。当前请求只保存在本页本地状态，不会进入真实队列。')
  }

  const handleSupport = (eventId) => {
    if (supportedEventIds.includes(eventId)) return
    setSupportedEventIds((current) => [...current, eventId])
    setSupportCounts((current) => ({ ...current, [eventId]: (current[eventId] || 0) + 1 }))
    setLocalNote('已在本地演示状态中记录支持。该数字不会提交到后端，也不代表真实热度或真实排序。')
  }

  const openBEndPanel = () => {
    setShowBEndPanel(true)
    setLocalNote('已展开企业 / 团队私有分析说明。当前不会提交信息、创建私有 case 或联系销售。')
  }

  return (
    <div className="page-stack public-event-page public-request-page">
      <section className="public-request-hero">
        <div>
          <div className="public-request-breadcrumb">公共事件广场 / Helldivers 事件 / 请求分析一个公共事件</div>
          <Space wrap>
            <Tag color="cyan">本地演示</Tag>
            <Tag>不提交到后端</Tag>
            <Tag>不代表自然舆情热度</Tag>
          </Space>
          <Title level={1}>请求分析一个公共事件</Title>
          <Paragraph>
            提交事件线索，帮助我们判断哪些公共事件适合做公开样本分析。当前为本地演示，不会提交到后端，不会触发抓取，不会调用真实平台 API 或真实 LLM。
          </Paragraph>
          <Space wrap>
            <Button icon={<ArrowLeft size={16} />} onClick={() => goToHash('#/public-events?guided=1')}>
              返回公共事件广场
            </Button>
            <Button icon={<ArrowLeft size={16} />} onClick={() => goToHash('#/public-events/helldivers-psn')}>
              返回 Helldivers 事件页
            </Button>
          </Space>
        </div>
        <Alert
          type="info"
          showIcon
          message="试玩最后一步"
          description="这是 C 端试玩流程的最后一步：请求更多事件，或了解企业 / 团队私有分析入口。请求数和支持数只用于本地演示，不代表自然公众热度。"
        />
      </section>

      {localNote ? (
        <Alert type="success" showIcon message="本地演示状态" description={localNote} closable onClose={() => setLocalNote('')} />
      ) : null}

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <TrackCard
            primary
            icon={<ClipboardList size={22} />}
            title="C 端轻量请求分析"
            description="适合普通用户、社区成员、创作者粉丝或事件关注者提交一个想看的公开事件线索。"
            tags={['公开事件线索', '本地预览', '不收集个人联系方式']}
          />
        </Col>
        <Col span={12}>
          <TrackCard
            icon={<Building2 size={22} />}
            title="企业 / 团队私有分析咨询"
            description="适合品牌、创作者、MCN、社区运营、游戏团队或公共关系团队了解私有 case / 报告服务入口。"
            tags={['私有语境', '证据复核', '报告导出']}
          />
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={14}>
          <Card
            className="panel-card public-request-form-card"
            title={
              <Space>
                <ClipboardList size={17} />
                <span>C 端轻量请求分析</span>
              </Space>
            }
          >
            <div className="public-request-form-grid">
              <label>
                <Text>事件名称</Text>
                <Input
                  value={formValues.title}
                  onChange={(event) => updateForm('title', event.target.value)}
                  placeholder="例如：某游戏账号绑定争议"
                />
              </label>
              <label>
                <Text>事件平台 / 场景</Text>
                <Select
                  value={formValues.eventType}
                  options={EVENT_TYPE_OPTIONS}
                  onChange={(value) => updateForm('eventType', value)}
                />
              </label>
              <label className="public-request-wide">
                <Text>相关链接 / 线索 URL</Text>
                <TextArea
                  value={formValues.publicLinks}
                  onChange={(event) => updateForm('publicLinks', event.target.value)}
                  placeholder="可粘贴公开新闻、论坛、视频、公告线索。当前页面不会抓取 URL 内容。"
                  rows={3}
                />
              </label>
              <label className="public-request-wide">
                <Text>补充平台 / 场景说明</Text>
                <Input
                  value={formValues.platformContext}
                  onChange={(event) => updateForm('platformContext', event.target.value)}
                  placeholder="例如：Steam 社区、Reddit 讨论、B 站评论区、品牌公告等"
                />
              </label>
              <label className="public-request-wide">
                <Text>为什么想看这个事件？</Text>
                <TextArea
                  value={formValues.reason}
                  onChange={(event) => updateForm('reason', event.target.value)}
                  placeholder="说明你想理解的问题，不要填写个人联系方式或敏感隐私信息。"
                  rows={4}
                />
              </label>
              <label className="public-request-wide">
                <Text>希望重点看什么？</Text>
                <Checkbox.Group
                  className="public-request-focus-options"
                  options={FOCUS_OPTIONS}
                  value={formValues.focusAreas}
                  onChange={(value) => updateForm('focusAreas', value)}
                />
              </label>
            </div>
            <Checkbox
              checked={formValues.attestedMock}
              onChange={(event) => updateForm('attestedMock', event.target.checked)}
            >
              我理解这只是本地演示入口，不会创建真实请求、真实投票或真实优先排序。
            </Checkbox>
            <Space className="public-request-action-row" wrap>
              <Button type="primary" onClick={submitPreview}>
                生成本地演示预览
              </Button>
              <Button onClick={() => { setFormValues(INITIAL_FORM); setPreview(null); setValidationMessage('') }}>
                清空
              </Button>
            </Space>
            {validationMessage ? <Alert type="warning" showIcon message={validationMessage} /> : null}
          </Card>
        </Col>
        <Col span={10}>
          <Card className="panel-card public-request-preview-card" title="本地演示预览">
            {preview ? (
              <Space direction="vertical" size={10}>
                <Space wrap>
                  <Tag color="cyan">本地演示请求</Tag>
                  <Tag>不进入真实队列</Tag>
                  <Tag>不触发抓取</Tag>
                  <Tag>不调用真实 API / LLM</Tag>
                </Space>
                <Title level={4}>{preview.title}</Title>
                <Paragraph>{preview.reason}</Paragraph>
                <div className="public-request-preview-grid">
                  <span>场景：{preview.eventType}</span>
                  <span>平台说明：{preview.platformContext}</span>
                  <span>重点：{preview.focusAreas.join(' / ')}</span>
                  <span>线索：{preview.publicLinks}</span>
                </div>
                <Alert
                  type="info"
                  showIcon
                  message="本地演示预览"
                  description="当前请求只保存在本页本地状态，不会进入真实队列，不会触发抓取，不会调用平台 API，不会调用 LLM。"
                />
              </Space>
            ) : (
              <Paragraph>
                填写左侧表单后，这里会生成本地预览卡。页面不提交到后端，不保存联系方式，也不会读取或抓取你粘贴的链接。
              </Paragraph>
            )}
          </Card>
        </Col>
      </Row>

      <section>
        <div className="public-event-section-title">
          <Text className="section-kicker">Local support demo</Text>
          <Title level={3}>支持候选事件</Title>
        </div>
        <Alert
          className="public-request-secondary-alert"
          type="info"
          showIcon
          message="支持数是次级本地演示"
          description="这里的支持数只用于本地 demo 展示，不代表自然舆情热度、真实公众需求、真实排序或真实排期，也不会提交到后端。"
        />
        <Row gutter={[16, 16]}>
          {supportCandidates.map((event) => (
            <Col span={6} key={event.event_id}>
              <SupportCandidateCard
                event={event}
                supported={supportedEventIds.includes(event.event_id)}
                supportCount={supportCounts[event.event_id] || event.vote_count_mock}
                onSupport={handleSupport}
              />
            </Col>
          ))}
        </Row>
      </section>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card
            className="panel-card public-request-explainer-card"
            title={
              <Space>
                <ShieldCheck size={17} />
                <span>透明优先分析说明</span>
              </Space>
            }
          >
            <Paragraph>
              未来如果开放优先分析或赞助分析，必须清楚标注来源、规则和限制；不能伪装成自然舆情热度，也不能影响证据结论。
            </Paragraph>
            <Paragraph>
              当前没有真实赞助、支付或优先排序系统；没有支付页面、价格、二维码或赞助提交。
            </Paragraph>
          </Card>
        </Col>
        <Col span={12}>
          <Card
            className="panel-card public-request-explainer-card"
            title={
              <Space>
                <Building2 size={17} />
                <span>企业 / 团队私有分析咨询</span>
              </Space>
            }
          >
            <Paragraph>
              适合品牌、公关、MCN、创作者、游戏社区、IP 运营或团队内部复盘。B 端私有分析可包含证据复核、样本覆盖说明、Opinion Ecosystem 摘要、风险点、回应节奏、报告导出和保密语境。
            </Paragraph>
            <Space wrap>
              <Button onClick={openBEndPanel}>查看私有分析说明</Button>
              <Button onClick={() => goToHash('#/reports/helldivers-psn-sample')}>查看报告样例</Button>
            </Space>
          </Card>
        </Col>
      </Row>

      {showBEndPanel ? (
        <Alert
          className="public-request-secondary-alert"
          type="info"
          showIcon
          message="企业 / 团队私有分析说明"
          description="当前不会提交信息，不会创建私有 case，不会联系销售。这里只展示未来 B 端服务入口：在合规数据来源和保密语境下，帮助团队做证据复核、风险报告、回应节奏和复盘分析。"
          closable
          onClose={() => setShowBEndPanel(false)}
        />
      ) : null}

      <Alert
        className="public-event-boundary-alert"
        type="info"
        showIcon
        icon={<Info size={18} />}
        message="请求 / 支持边界"
        description="当前为本地演示；不会提交到后端；不会创建真实请求；不会写入真实投票；不会触发抓取；不会调用真实平台 API；不会调用真实 LLM；支持数 / 请求数不代表自然舆情热度；当前没有真实赞助、支付或优先排序系统。"
      />
    </div>
  )
}
