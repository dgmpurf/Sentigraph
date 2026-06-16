import { Alert, Button, Card, Checkbox, Col, Input, Row, Select, Space, Tag, Typography } from 'antd'
import { ArrowLeft, Building2, CheckCircle2, ClipboardList, ShieldCheck, Vote } from 'lucide-react'
import { useMemo, useState } from 'react'

import { PUBLIC_EVENT_PLAZA_EVENTS } from '../data/publicEventSamples.js'

const { Paragraph, Text, Title } = Typography
const { TextArea } = Input

const EVENT_TYPE_OPTIONS = [
  { label: '游戏', value: 'game' },
  { label: '动漫', value: 'anime' },
  { label: '品牌', value: 'brand' },
  { label: '创作者', value: 'creator' },
  { label: '社区', value: 'community' },
  { label: '产品', value: 'product' },
  { label: '其他', value: 'other' },
]

const URGENCY_OPTIONS = [
  { label: '低', value: 'low' },
  { label: '中', value: 'medium' },
  { label: '高', value: 'high' },
]

const INITIAL_FORM = {
  title: '',
  eventType: 'game',
  publicLinks: '',
  reason: '',
  urgency: 'medium',
  attestedMock: false,
}

function VoteCandidateCard({ event, supported, voteCount, onVote }) {
  return (
    <Card className="panel-card public-request-vote-card">
      <Space direction="vertical" size={10} className="full-width">
        <Space wrap>
          <Tag color="cyan">{event.event_type_label}</Tag>
          <Tag>{event.sample_label}</Tag>
          <Tag color={event.is_sample_available ? 'green' : 'gold'}>{event.queue_label}</Tag>
        </Space>
        <div>
          <Title level={4}>{event.title}</Title>
          <Paragraph>{event.request_note}</Paragraph>
        </div>
        <div className="public-request-count-grid">
          <div>
            <Text type="secondary">request mock</Text>
            <strong>{event.request_count_mock}</strong>
          </div>
          <div>
            <Text type="secondary">vote mock</Text>
            <strong>{voteCount}</strong>
          </div>
        </div>
        <Button
          icon={supported ? <CheckCircle2 size={16} /> : <Vote size={16} />}
          disabled={event.is_sample_available || supported}
          onClick={() => onVote(event.event_id)}
          type={supported ? 'default' : 'primary'}
        >
          {event.is_sample_available ? '已有样本 / 查看分析' : supported ? '已支持（本地 mock）' : event.vote_cta_label}
        </Button>
        <Text type="secondary">这只是本地 mock，不提交到后端，也不代表真实热度。</Text>
      </Space>
    </Card>
  )
}

export function PublicEventRequest() {
  const voteCandidates = useMemo(
    () => PUBLIC_EVENT_PLAZA_EVENTS.filter((event) => !event.is_sample_available).slice(0, 4),
    [],
  )
  const initialVoteCounts = useMemo(
    () => Object.fromEntries(voteCandidates.map((event) => [event.event_id, event.vote_count_mock])),
    [voteCandidates],
  )
  const [formValues, setFormValues] = useState(INITIAL_FORM)
  const [validationMessage, setValidationMessage] = useState('')
  const [preview, setPreview] = useState(null)
  const [supportedEventIds, setSupportedEventIds] = useState([])
  const [voteCounts, setVoteCounts] = useState(initialVoteCounts)
  const [localNote, setLocalNote] = useState('')

  const goToHash = (hash) => {
    window.location.hash = hash
  }

  const updateForm = (field, value) => {
    setFormValues((current) => ({ ...current, [field]: value }))
  }

  const submitPreview = () => {
    if (!formValues.title.trim() || !formValues.reason.trim() || !formValues.attestedMock) {
      setValidationMessage('请填写事件标题、请求理由，并确认这是不会真实提交的 mock 入口。')
      setPreview(null)
      return
    }

    setValidationMessage('')
    setPreview({
      title: formValues.title.trim(),
      eventType: EVENT_TYPE_OPTIONS.find((option) => option.value === formValues.eventType)?.label || formValues.eventType,
      publicLinks: formValues.publicLinks.trim() || '未填写公开链接',
      reason: formValues.reason.trim(),
      urgency: URGENCY_OPTIONS.find((option) => option.value === formValues.urgency)?.label || formValues.urgency,
    })
  }

  const handleVote = (eventId) => {
    if (supportedEventIds.includes(eventId)) return
    setSupportedEventIds((current) => [...current, eventId])
    setVoteCounts((current) => ({ ...current, [eventId]: (current[eventId] || 0) + 1 }))
    setLocalNote('已在本地 mock 状态中记录支持。该数字不会提交到后端，也不代表真实热度。')
  }

  const handleBEndClick = () => {
    setLocalNote('当前为 mock 入口，未来可用于品牌、MCN、创作者、公关团队、游戏社区运营的私有分析咨询。')
  }

  return (
    <div className="page-stack public-event-page public-request-page">
      <section className="public-request-hero">
        <div>
          <div className="public-request-breadcrumb">公共事件广场 / Helldivers 事件 / 请求分析类似事件</div>
          <Space wrap>
            <Tag color="cyan">frontend-only mock</Tag>
            <Tag>no backend submission</Tag>
            <Tag>not natural heat</Tag>
          </Space>
          <Title level={1}>请求分析 / 投票支持分析</Title>
          <Paragraph>
            你可以请求 Sentigraph 分析一个公共事件。当前不会提交到后端；请求/投票数量不代表自然舆情热度；赞助分析必须透明标注。
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
          message="v1 边界"
          description="本页不支持隐藏推广或伪造热度，没有真实支付、真实账号、真实提交、真实平台动作，也不会调用 API 或 LLM。"
        />
      </section>

      {localNote ? <Alert type="success" showIcon message="本地试玩状态" description={localNote} closable onClose={() => setLocalNote('')} /> : null}

      <Row gutter={[16, 16]}>
        <Col span={14}>
          <Card
            className="panel-card public-request-form-card"
            title={
              <Space>
                <ClipboardList size={17} />
                <span>生成本地请求预览</span>
              </Space>
            }
          >
            <div className="public-request-form-grid">
              <label>
                <Text>事件标题</Text>
                <Input
                  value={formValues.title}
                  onChange={(event) => updateForm('title', event.target.value)}
                  placeholder="例如：某游戏版本更新争议"
                />
              </label>
              <label>
                <Text>事件类型</Text>
                <Select
                  value={formValues.eventType}
                  options={EVENT_TYPE_OPTIONS}
                  onChange={(value) => updateForm('eventType', value)}
                />
              </label>
              <label>
                <Text>紧急度</Text>
                <Select
                  value={formValues.urgency}
                  options={URGENCY_OPTIONS}
                  onChange={(value) => updateForm('urgency', value)}
                />
              </label>
              <label className="public-request-wide">
                <Text>公开链接（可选）</Text>
                <TextArea
                  value={formValues.publicLinks}
                  onChange={(event) => updateForm('publicLinks', event.target.value)}
                  placeholder="可粘贴公开新闻、论坛、视频、公告链接。当前不会抓取 URL。"
                  rows={3}
                />
              </label>
              <label className="public-request-wide">
                <Text>请求理由</Text>
                <TextArea
                  value={formValues.reason}
                  onChange={(event) => updateForm('reason', event.target.value)}
                  placeholder="为什么这个事件值得分析？你希望理解什么？"
                  rows={4}
                />
              </label>
            </div>
            <Checkbox
              checked={formValues.attestedMock}
              onChange={(event) => updateForm('attestedMock', event.target.checked)}
            >
              我理解这是 mock 入口，不会真实提交。
            </Checkbox>
            <Space className="public-request-action-row" wrap>
              <Button type="primary" onClick={submitPreview}>
                生成本地请求预览
              </Button>
              <Button onClick={() => { setFormValues(INITIAL_FORM); setPreview(null); setValidationMessage('') }}>
                清空
              </Button>
            </Space>
            {validationMessage ? <Alert type="warning" showIcon message={validationMessage} /> : null}
          </Card>
        </Col>
        <Col span={10}>
          <Card className="panel-card public-request-preview-card" title="Local preview / 本地预览">
            {preview ? (
              <Space direction="vertical" size={10}>
                <Space wrap>
                  <Tag color="cyan">user-requested mock</Tag>
                  <Tag color="default">not natural heat</Tag>
                  <Tag color="default">not official verification</Tag>
                  <Tag color="default">not causal proof</Tag>
                </Space>
                <Title level={4}>{preview.title}</Title>
                <Paragraph>{preview.reason}</Paragraph>
                <div className="public-request-preview-grid">
                  <span>类型：{preview.eventType}</span>
                  <span>紧急度：{preview.urgency}</span>
                  <span>状态：local mock only</span>
                  <span>链接：{preview.publicLinks}</span>
                </div>
              </Space>
            ) : (
              <Paragraph>填写左侧表单后，这里会生成本地预览卡。不会提交到后端，也不会抓取链接内容。</Paragraph>
            )}
          </Card>
        </Col>
      </Row>

      <section>
        <div className="public-event-section-title">
          <Text className="section-kicker">Vote mock</Text>
          <Title level={3}>投票支持分析候选事件</Title>
        </div>
        <Row gutter={[16, 16]}>
          {voteCandidates.map((event) => (
            <Col span={6} key={event.event_id}>
              <VoteCandidateCard
                event={event}
                supported={supportedEventIds.includes(event.event_id)}
                voteCount={voteCounts[event.event_id] || event.vote_count_mock}
                onVote={handleVote}
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
                <span>赞助分析 / 优先推演必须透明标注</span>
              </Space>
            }
          >
            <Paragraph>
              未来赞助分析可以作为排期或优先推演信号，但必须显著标注来源，不能混入自然热度，也不能隐藏赞助/请求背景。
            </Paragraph>
            <Paragraph>v1 没有真实支付流程，没有真实赞助状态，也没有任何后端提交。</Paragraph>
          </Card>
        </Col>
        <Col span={12}>
          <Card
            className="panel-card public-request-explainer-card"
            title={
              <Space>
                <Building2 size={17} />
                <span>需要私有分析？</span>
              </Space>
            }
          >
            <Paragraph>
              私有分析可面向品牌、MCN、创作者、公关团队和游戏社区运营，后续可包含更深证据复核、保密语境、丰富报告和场景对比。
            </Paragraph>
            <Button onClick={handleBEndClick}>B端咨询（mock）</Button>
          </Card>
        </Col>
      </Row>

      <Alert
        className="public-event-boundary-alert"
        type="info"
        showIcon
        message="请求/投票边界"
        description="本页是 frontend-only mock。请求和投票只保存在本地 UI 状态，不代表 full-web coverage、full-platform coverage、official verification、causal proof，不执行真实平台动作，不调用真实 API 或 LLM。PeopleCluster 是人群簇，不是真实个人；InfluenceCore 是内容/叙事/官方/媒体/梗核心。"
      />
    </div>
  )
}
