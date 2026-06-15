import { Card, Col, Progress, Row, Space, Statistic, Tag, Timeline, Typography } from 'antd'
import { Activity, Boxes, CircleDot, Clock3, Compass, RadioTower, Sparkles } from 'lucide-react'
import { useEffect, useMemo, useRef } from 'react'

import { BOX_HEIGHT, BOX_WIDTH, campStateToVisual, scoreToPercent } from '../../data/opinionEcosystemMock.js'

const { Paragraph, Text, Title } = Typography

const TIMELINE_STEPS = [
  { key: 't0', label: 'T0 事件触发', scenarios: ['natural', 'no_response', 'delayed_response'] },
  { key: 't1', label: 'T1 社区反弹', scenarios: ['natural', 'delayed_response', 'no_response'] },
  { key: 't2', label: 'T2 官方回应', scenarios: ['official_clarification', 'faq_explainer'] },
  { key: 't3', label: 'T3 第三方说明', scenarios: ['third_party_explanation'] },
  { key: 't4', label: 'T4 解构窗口', scenarios: ['community_deconstruction'] },
  { key: 't5', label: 'T5 疲劳衰减', scenarios: ['faq_explainer', 'community_deconstruction'] },
  { key: 't6', label: 'T6 声誉记忆', scenarios: ['delayed_response', 'no_response'] },
]

const EVENT_TOKENS = [
  { key: 'official_clarification', label: '官方澄清', coreId: 'official' },
  { key: 'faq_explainer', label: 'FAQ / 长文解释', coreId: 'third_party' },
  { key: 'third_party_explanation', label: '第三方说明', coreId: 'third_party' },
  { key: 'media_amplification', label: '媒体放大', coreId: 'opposition' },
  { key: 'community_deconstruction', label: '社区解构', coreId: 'deconstruction' },
  { key: 'delayed_response', label: '延迟回应', coreId: 'opposition' },
  { key: 'no_response', label: '无回应基线', coreId: 'opposition' },
]

const CORE_ROLE_LABELS = {
  opposition: 'Community backlash core',
  official: 'Official statement core',
  third_party: 'Third-party explanation core',
  deconstruction: 'Meme / deconstruction core',
}

const DYNAMICS_LABELS = [
  ['同化', 'soft clusters moving toward a stronger narrative core'],
  ['中立化', 'opposed or supportive clusters cooling toward gray/yellow'],
  ['退出', 'fatigued clusters fading toward the boundary'],
  ['固化', 'high-identity clusters locking around a core'],
  ['反噬', 'poor timing increasing hardening or opposition pull'],
  ['再激活', 'dormant grievance reappearing after a shock event'],
]

function drawRoundedRect(ctx, x, y, width, height, radius) {
  ctx.beginPath()
  ctx.moveTo(x + radius, y)
  ctx.arcTo(x + width, y, x + width, y + height, radius)
  ctx.arcTo(x + width, y + height, x, y + height, radius)
  ctx.arcTo(x, y + height, x, y, radius)
  ctx.arcTo(x, y, x + radius, y, radius)
  ctx.closePath()
}

function drawEchoBoundary(ctx, scenario, tick) {
  const echo = scenario.echoBox.echo_chamber_score
  const breakout = scenario.echoBox.breakout_risk
  const permeability = scenario.echoBox.permeability_score
  const saturation = scenario.echoBox.saturation_ratio
  const pulse = Math.sin(tick * 0.025) * breakout * 6
  const inset = 18 - pulse
  const width = BOX_WIDTH - inset * 2
  const height = BOX_HEIGHT - inset * 2
  const borderWidth = 3 + echo * 9

  ctx.save()
  const gradient = ctx.createRadialGradient(BOX_WIDTH * 0.52, BOX_HEIGHT * 0.48, 40, BOX_WIDTH * 0.5, BOX_HEIGHT * 0.5, 520)
  gradient.addColorStop(0, `rgba(66, 245, 215, ${0.09 + saturation * 0.12})`)
  gradient.addColorStop(0.45, `rgba(120, 166, 255, ${0.04 + saturation * 0.06})`)
  gradient.addColorStop(1, `rgba(255, 93, 143, ${0.04 + breakout * 0.08})`)
  ctx.fillStyle = gradient
  drawRoundedRect(ctx, inset, inset, width, height, 26)
  ctx.fill()

  ctx.shadowColor = '#42f5d7'
  ctx.shadowBlur = 14 + breakout * 32
  ctx.strokeStyle = `rgba(66, 245, 215, ${0.36 + echo * 0.48})`
  ctx.lineWidth = borderWidth
  drawRoundedRect(ctx, inset, inset, width, height, 26)
  ctx.stroke()

  ctx.shadowBlur = 0
  ctx.lineWidth = Math.max(2, borderWidth - 2)
  ctx.strokeStyle = 'rgba(8, 9, 13, 0.86)'
  const gapSize = 42 + permeability * 68
  const gaps = [
    [BOX_WIDTH * 0.5 - gapSize / 2, inset, gapSize, 0],
    [BOX_WIDTH - inset, BOX_HEIGHT * 0.52 - gapSize / 2, 0, gapSize],
    [BOX_WIDTH * 0.32 - gapSize / 2, BOX_HEIGHT - inset, gapSize, 0],
  ]
  gaps.forEach(([x, y, dx, dy]) => {
    ctx.beginPath()
    ctx.moveTo(x, y)
    ctx.lineTo(x + dx, y + dy)
    ctx.stroke()
  })

  ctx.strokeStyle = `rgba(255, 93, 143, ${0.16 + breakout * 0.36})`
  ctx.lineWidth = 1.4
  for (let i = 0; i < 5; i += 1) {
    const crackX = inset + 42 + i * 138
    const crackY = inset + 8 + Math.sin(tick * 0.02 + i) * 10
    ctx.beginPath()
    ctx.moveTo(crackX, crackY)
    ctx.lineTo(crackX + 16, crackY + 18 + breakout * 16)
    ctx.lineTo(crackX + 8, crackY + 42)
    ctx.stroke()
  }

  ctx.fillStyle = '#dffbf7'
  ctx.font = '700 14px "Microsoft YaHei", sans-serif'
  ctx.fillText('EchoBox / 回音壁容器', inset + 16, inset + 28)
  ctx.restore()
}

function drawGrid(ctx) {
  ctx.save()
  ctx.strokeStyle = 'rgba(154, 166, 191, 0.07)'
  ctx.lineWidth = 1
  for (let x = 44; x < BOX_WIDTH; x += 44) {
    ctx.beginPath()
    ctx.moveTo(x, 28)
    ctx.lineTo(x, BOX_HEIGHT - 28)
    ctx.stroke()
  }
  for (let y = 44; y < BOX_HEIGHT; y += 44) {
    ctx.beginPath()
    ctx.moveTo(28, y)
    ctx.lineTo(BOX_WIDTH - 28, y)
    ctx.stroke()
  }
  ctx.restore()
}

function drawCore(ctx, core, scenario, tick) {
  const pull = core.gravitational_pull
  const aura = 42 + pull * 110 + Math.sin(tick * 0.03 + core.core_id.length) * pull * 8
  const size = 18 + pull * 28
  const roleLabel = CORE_ROLE_LABELS[core.core_id] || core.core_type
  const isDeconstruction = core.core_id === 'deconstruction'
  const isOfficial = core.core_id === 'official'

  ctx.save()
  ctx.translate(core.position.x, core.position.y)
  ctx.strokeStyle = `${core.visual_color}44`
  ctx.fillStyle = `${core.visual_color}0f`
  ctx.lineWidth = 1.2
  ctx.beginPath()
  ctx.arc(0, 0, aura, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()

  ctx.shadowColor = core.visual_color
  ctx.shadowBlur = 22 + pull * 30
  ctx.fillStyle = `${core.visual_color}30`
  ctx.strokeStyle = core.visual_color
  ctx.lineWidth = 2.2

  if (isOfficial) {
    ctx.beginPath()
    ctx.rect(-size, -size, size * 2, size * 2)
  } else if (isDeconstruction) {
    ctx.beginPath()
    for (let i = 0; i < 5; i += 1) {
      const angle = -Math.PI / 2 + (i * Math.PI * 2) / 5
      const radius = i % 2 === 0 ? size * 1.18 : size * 0.72
      const x = Math.cos(angle) * radius
      const y = Math.sin(angle) * radius
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }
    ctx.closePath()
  } else {
    ctx.beginPath()
    for (let i = 0; i < 6; i += 1) {
      const angle = Math.PI / 6 + (i * Math.PI * 2) / 6
      const x = Math.cos(angle) * size
      const y = Math.sin(angle) * size
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }
    ctx.closePath()
  }
  ctx.fill()
  ctx.stroke()

  ctx.shadowBlur = 0
  ctx.strokeStyle = `rgba(244, 247, 251, ${0.24 + pull * 0.5})`
  ctx.lineWidth = 1
  ctx.beginPath()
  ctx.arc(0, 0, size + 8, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * pull)
  ctx.stroke()

  ctx.fillStyle = '#eef4ff'
  ctx.font = '700 12px "Microsoft YaHei", sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText(core.label, 0, size + 20)
  ctx.fillStyle = 'rgba(214, 222, 239, 0.72)'
  ctx.font = '11px "Microsoft YaHei", sans-serif'
  ctx.fillText(roleLabel, 0, size + 36)

  if (scenario.scenarioKey === 'community_deconstruction' && isDeconstruction) {
    ctx.fillStyle = '#f5c44b'
    ctx.font = '700 10px "Microsoft YaHei", sans-serif'
    ctx.fillText('deconstruction marker', 0, -size - 12)
  }
  ctx.restore()
}

function drawPeopleCluster(ctx, cluster, scenario, tick) {
  const visual = campStateToVisual(cluster.camp_state, cluster)
  const isWithdrawn = cluster.camp_state === 'withdrawn'
  const isDormant = cluster.camp_state === 'dormant_grievance'
  const fatigueOpacity = Math.max(0.2, 1 - cluster.fatigue * 0.74)
  const opacity = isWithdrawn ? 0.16 : fatigueOpacity
  const highEmotionBoost = 1 + cluster.expression_intensity * 0.18
  const pulse = 1 + Math.sin(tick * (0.036 + cluster.activity_weight * 0.018) + cluster.phase) * 0.09 * highEmotionBoost
  const radius = (3 + cluster.population_weight * 4.4 + cluster.influence_weight * 2.4) * pulse
  const outlineColor = isDormant ? '#1b1020' : cluster.bridge_power > 0.74 ? '#d9c6ff' : 'rgba(244, 247, 251, 0.24)'

  ctx.save()
  ctx.globalAlpha = opacity
  ctx.shadowColor = visual.color
  ctx.shadowBlur = 4 + cluster.expression_intensity * 13
  ctx.fillStyle = visual.color
  ctx.beginPath()
  ctx.arc(cluster.position.x, cluster.position.y, radius, 0, Math.PI * 2)
  ctx.fill()
  ctx.shadowBlur = 0
  ctx.globalAlpha = Math.min(0.92, opacity + 0.16)
  ctx.strokeStyle = outlineColor
  ctx.lineWidth = isDormant ? 2.2 : cluster.bridge_power > 0.74 ? 1.6 : 0.8
  ctx.stroke()
  ctx.restore()
}

function drawBridgeLinks(ctx, scenario, peopleClusters) {
  const cores = new Map(scenario.influenceCores.map((core) => [core.core_id, core]))
  ctx.save()
  peopleClusters
    .filter((cluster) => cluster.bridge_power > 0.74 && cluster.camp_state !== 'withdrawn')
    .slice(0, 22)
    .forEach((cluster, index) => {
      const target = cores.get(index % 2 === 0 ? 'third_party' : 'deconstruction') || scenario.influenceCores[0]
      if (!target) return
      ctx.strokeStyle = 'rgba(164, 120, 255, 0.2)'
      ctx.lineWidth = 0.9
      ctx.beginPath()
      ctx.moveTo(cluster.position.x, cluster.position.y)
      ctx.quadraticCurveTo(BOX_WIDTH / 2, BOX_HEIGHT / 2, target.position.x, target.position.y)
      ctx.stroke()
    })
  ctx.restore()
}

function drawEventTokenLink(ctx, scenarioKey, scenario, tick) {
  const activeToken = EVENT_TOKENS.find((token) => token.key === scenarioKey) || EVENT_TOKENS[0]
  const target = scenario.influenceCores.find((core) => core.core_id === activeToken.coreId)
  if (!target) return
  const progress = (Math.sin(tick * 0.035) + 1) / 2
  const start = { x: BOX_WIDTH - 66, y: 40 }
  const x = start.x + (target.position.x - start.x) * progress
  const y = start.y + (target.position.y - start.y) * progress

  ctx.save()
  ctx.strokeStyle = 'rgba(245, 196, 75, 0.32)'
  ctx.setLineDash([7, 7])
  ctx.lineWidth = 1.2
  ctx.beginPath()
  ctx.moveTo(start.x, start.y)
  ctx.lineTo(target.position.x, target.position.y)
  ctx.stroke()
  ctx.setLineDash([])
  ctx.fillStyle = '#f5c44b'
  ctx.shadowColor = '#f5c44b'
  ctx.shadowBlur = 14
  ctx.beginPath()
  ctx.arc(x, y, 5, 0, Math.PI * 2)
  ctx.fill()
  ctx.restore()
}

function drawV2Sandbox(ctx, scenario, peopleClusters, tick) {
  ctx.clearRect(0, 0, BOX_WIDTH, BOX_HEIGHT)
  drawEchoBoundary(ctx, scenario, tick)
  drawGrid(ctx)
  drawEventTokenLink(ctx, scenario.scenarioKey, scenario, tick)
  drawBridgeLinks(ctx, scenario, peopleClusters)
  scenario.influenceCores.forEach((core) => drawCore(ctx, core, scenario, tick))
  peopleClusters.forEach((cluster) => drawPeopleCluster(ctx, cluster, scenario, tick))
}

function MetricProgress({ label, value, color }) {
  return (
    <div className="ecosystem-v2-progress-row">
      <Text>{label}</Text>
      <Progress percent={scoreToPercent(value)} size="small" strokeColor={color} trailColor="rgba(154,166,191,0.18)" />
    </div>
  )
}

function ScenarioTokenStrip({ scenarioKey }) {
  return (
    <div className="ecosystem-v2-event-strip">
      {EVENT_TOKENS.map((token) => (
        <span key={token.key} className={token.key === scenarioKey ? 'active' : ''}>
          {token.label}
        </span>
      ))}
    </div>
  )
}

function ResponseTimeline({ scenarioKey }) {
  return (
    <Timeline
      className="ecosystem-v2-timeline"
      items={TIMELINE_STEPS.map((step) => ({
        color: step.scenarios.includes(scenarioKey) ? '#42f5d7' : 'gray',
        children: (
          <span className={step.scenarios.includes(scenarioKey) ? 'active' : ''}>
            {step.label}
          </span>
        ),
      }))}
    />
  )
}

export function OpinionEcosystemV2Canvas({ scenarioView, peopleClusters, metrics, playing }) {
  const canvasRef = useRef(null)
  const latestRef = useRef({ scenarioView, peopleClusters, playing })
  const frameRef = useRef(null)
  const localTickRef = useRef(0)

  latestRef.current = { scenarioView, peopleClusters, playing }

  useEffect(() => {
    const draw = () => {
      const canvas = canvasRef.current
      if (!canvas) return
      const ratio = window.devicePixelRatio || 1
      if (canvas.width !== BOX_WIDTH * ratio || canvas.height !== BOX_HEIGHT * ratio) {
        canvas.width = BOX_WIDTH * ratio
        canvas.height = BOX_HEIGHT * ratio
        canvas.style.width = `${BOX_WIDTH}px`
        canvas.style.height = `${BOX_HEIGHT}px`
      }
      const context = canvas.getContext('2d')
      if (!context) return
      if (latestRef.current.playing) localTickRef.current += 1
      context.setTransform(ratio, 0, 0, ratio, 0, 0)
      drawV2Sandbox(context, latestRef.current.scenarioView, latestRef.current.peopleClusters, localTickRef.current)
      frameRef.current = requestAnimationFrame(draw)
    }
    frameRef.current = requestAnimationFrame(draw)
    return () => {
      if (frameRef.current) cancelAnimationFrame(frameRef.current)
    }
  }, [])

  const activeTimeline = useMemo(
    () => TIMELINE_STEPS.find((step) => step.scenarios.includes(scenarioView.scenarioKey)) || TIMELINE_STEPS[0],
    [scenarioView.scenarioKey],
  )

  return (
    <div className="ecosystem-v2-shell">
      <Row gutter={[16, 16]}>
        <Col span={18}>
          <Card
            className="panel-card ecosystem-v2-stage-card"
            title={
              <Space>
                <Boxes size={18} />
                <span>V2 Ecology View / EchoBox 主舞台</span>
              </Space>
            }
            extra={
              <Space wrap>
                <Tag color={playing ? 'green' : 'default'}>{playing ? 'playing' : 'paused'}</Tag>
                <Tag color="cyan">{activeTimeline.label}</Tag>
              </Space>
            }
          >
            <div className="ecosystem-v2-topline">
              <ScenarioTokenStrip scenarioKey={scenarioView.scenarioKey} />
            </div>
            <div
              className="ecosystem-v2-canvas-frame"
              style={{
                '--v2-echo-alpha': `${0.24 + scenarioView.echoBox.echo_chamber_score * 0.52}`,
                '--v2-breakout-alpha': `${0.12 + scenarioView.echoBox.breakout_risk * 0.38}`,
              }}
            >
              <canvas ref={canvasRef} aria-label="Opinion Ecosystem Sandbox v2 ecology canvas" />
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="panel-card ecosystem-v2-side-card" title="V2 metrics / 状态读数">
            <div className="ecosystem-v2-stat-grid">
              <Statistic title="阵营分布" value={peopleClusters.length} suffix="簇" />
              <Statistic title="破圈风险" value={scoreToPercent(metrics.breakoutRisk)} suffix="%" />
              <Statistic title="饱和度" value={scoreToPercent(metrics.echoBoxSaturation)} suffix="%" />
              <Statistic title="解构窗口" value={scoreToPercent(metrics.deconstructionWindow)} suffix="%" />
            </div>
            <MetricProgress label="中立化趋势" value={scenarioView.campDynamics.neutralization_score} color="#42f5d7" />
            <MetricProgress label="退出 / 疲劳" value={scenarioView.campDynamics.withdrawal_score} color="#667085" />
            <MetricProgress label="反噬风险" value={scenarioView.campDynamics.backlash_score} color="#ff5d8f" />
            <MetricProgress label="Dormant grievance risk" value={metrics.dormantGrievanceRisk} color="#f5c44b" />
            <div className="ecosystem-v2-note">
              <Text type="secondary">Scenario annotation</Text>
              <Paragraph>{scenarioView.responseTempo.recommendation_text}</Paragraph>
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={8}>
          <Card className="panel-card ecosystem-v2-card" title="Response Tempo / 时间轴">
            <ResponseTimeline scenarioKey={scenarioView.scenarioKey} />
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card ecosystem-v2-card" title="Camp Dynamics / 阵营动力">
            <div className="ecosystem-v2-dynamics-grid">
              {DYNAMICS_LABELS.map(([label, description]) => (
                <div key={label}>
                  <Text strong>{label}</Text>
                  <Paragraph>{description}</Paragraph>
                </div>
              ))}
            </div>
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card ecosystem-v2-card" title="How to read V2 / 快速阅读">
            <Space direction="vertical" size={10}>
              <Space>
                <CircleDot size={15} />
                <Text>小球是匿名 PeopleCluster，不是真实个人。</Text>
              </Space>
              <Space>
                <RadioTower size={15} />
                <Text>大节点是 InfluenceCore，代表内容/叙事/官方/媒体/梗核心。</Text>
              </Space>
              <Space>
                <Compass size={15} />
                <Text>边界越厚表示 EchoBox 越强，缺口表示可渗透。</Text>
              </Space>
              <Space>
                <Clock3 size={15} />
                <Text>时间轴展示响应节奏，不代表因果证明。</Text>
              </Space>
              <Space>
                <Activity size={15} />
                <Text>指标是辅助说明，不代表全网/全平台覆盖。</Text>
              </Space>
            </Space>
          </Card>
        </Col>
      </Row>

      <Card
        className="panel-card ecosystem-v2-safety-card"
        title={
          <Space>
            <Sparkles size={18} />
            <span>V2 safety boundary / 安全边界</span>
          </Space>
        }
      >
        <Space wrap>
          <Tag color="cyan">frontend-only local prototype</Tag>
          <Tag>mock/local fixture data</Tag>
          <Tag>not full-web coverage</Tag>
          <Tag>not full-platform coverage</Tag>
          <Tag>not official verification</Tag>
          <Tag>not causal proof</Tag>
          <Tag>no real platform action</Tag>
          <Tag>no real APIs or LLMs</Tag>
          <Tag>PeopleCluster = anonymous groups</Tag>
          <Tag>InfluenceCore = content / narrative cores</Tag>
        </Space>
      </Card>
    </div>
  )
}
