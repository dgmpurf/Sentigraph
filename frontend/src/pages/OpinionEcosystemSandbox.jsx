import { Alert, Button, Card, Col, List, Progress, Row, Segmented, Space, Statistic, Tag, Typography } from 'antd'
import { PauseCircle, PlayCircle, RotateCcw, ScanLine, Sparkles } from 'lucide-react'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

const { Paragraph, Text, Title } = Typography

const BOX_WIDTH = 760
const BOX_HEIGHT = 520
const PARTICLE_COUNT = 164

const STATE_COLORS = {
  support: '#54f5a8',
  neutral: '#a7b0c4',
  oppose: '#ff5d8f',
  uncertain: '#f5c44b',
  bridge: '#a478ff',
  withdrawn: '#667085',
}

const STATE_LABELS = {
  support: '温和支持',
  neutral: '中立参与',
  oppose: '温和反对',
  uncertain: '摇摆观望',
  bridge: '桥接人群簇',
  withdrawn: '退出讨论',
}

const SCENARIOS = {
  natural: {
    label: '自然演化',
    tempo: '观察 2-4 小时后补充事实',
    echoStrength: 0.58,
    neutralization: 0.16,
    fatigue: 0.22,
    deconstruction: 0.08,
    hardening: 0.16,
    breakout: 0.32,
    pull: {
      opposition: 0.42,
      official: 0.12,
      thirdParty: 0.08,
      deconstruct: 0.04,
    },
    recommendation: '当前更适合补充事实说明，不建议强行解构。',
  },
  official: {
    label: '官方澄清',
    tempo: '先给事实边界，再承诺更新时间',
    echoStrength: 0.48,
    neutralization: 0.34,
    fatigue: 0.18,
    deconstruction: 0.12,
    hardening: 0.12,
    breakout: 0.24,
    pull: {
      opposition: 0.28,
      official: 0.42,
      thirdParty: 0.14,
      deconstruct: 0.08,
    },
    recommendation: '温和反对者存在中立化窗口，适合发布可核验事实说明。',
  },
  faq: {
    label: 'FAQ / 长文解释',
    tempo: '降低重复误解，维持稳定更新',
    echoStrength: 0.43,
    neutralization: 0.42,
    fatigue: 0.2,
    deconstruction: 0.2,
    hardening: 0.1,
    breakout: 0.18,
    pull: {
      opposition: 0.24,
      official: 0.3,
      thirdParty: 0.34,
      deconstruct: 0.14,
    },
    recommendation: '重复疑问较多时，FAQ 比高频短回应更能降低回音壁饱和度。',
  },
  thirdParty: {
    label: '第三方说明',
    tempo: '用独立事实链辅助澄清',
    echoStrength: 0.4,
    neutralization: 0.38,
    fatigue: 0.18,
    deconstruction: 0.24,
    hardening: 0.1,
    breakout: 0.2,
    pull: {
      opposition: 0.2,
      official: 0.16,
      thirdParty: 0.48,
      deconstruct: 0.18,
    },
    recommendation: '第三方说明适合承接事实争议，但仍需保留人工复核和来源说明。',
  },
  deconstruct: {
    label: '社区解构',
    tempo: '轻量解释，避免扩圈',
    echoStrength: 0.36,
    neutralization: 0.44,
    fatigue: 0.28,
    deconstruction: 0.54,
    hardening: 0.08,
    breakout: 0.16,
    pull: {
      opposition: 0.18,
      official: 0.14,
      thirdParty: 0.2,
      deconstruct: 0.56,
    },
    recommendation: '当前 EchoBox 高热但外溢弱，轻量解构可降低冲突表达强度。',
  },
  delayed: {
    label: '延迟回应',
    tempo: '需补充阶段性说明，避免空窗',
    echoStrength: 0.72,
    neutralization: 0.08,
    fatigue: 0.12,
    deconstruction: 0.04,
    hardening: 0.32,
    breakout: 0.48,
    pull: {
      opposition: 0.58,
      official: 0.04,
      thirdParty: 0.04,
      deconstruct: 0.02,
    },
    recommendation: '声量下降不等于问题解决，存在潜伏反噬风险。',
  },
  none: {
    label: '无回应',
    tempo: '仅作为基线，不建议长期使用',
    echoStrength: 0.8,
    neutralization: 0.04,
    fatigue: 0.08,
    deconstruction: 0.02,
    hardening: 0.44,
    breakout: 0.58,
    pull: {
      opposition: 0.66,
      official: 0.02,
      thirdParty: 0.02,
      deconstruct: 0.01,
    },
    recommendation: '无回应基线下，反噬风险和潜伏不满会继续累积。',
  },
}

const SCENARIO_OPTIONS = Object.entries(SCENARIOS).map(([value, scenario]) => ({
  value,
  label: scenario.label,
}))

const CORE_NODES = [
  {
    id: 'opposition',
    label: '反方核心视频',
    type: '内容核心',
    x: 178,
    y: 130,
    color: '#ff5d8f',
    note: '高冲突叙事的聚集点，不代表真实个人。',
  },
  {
    id: 'official',
    label: '官方说明',
    type: '官方核心',
    x: 560,
    y: 150,
    color: '#42f5d7',
    note: '用于事实边界和处理节奏说明。',
  },
  {
    id: 'thirdParty',
    label: '第三方解释',
    type: '解释核心',
    x: 510,
    y: 386,
    color: '#78a6ff',
    note: '承接可核验事实链，降低误读。',
  },
  {
    id: 'deconstruct',
    label: '社区解构梗',
    type: '解构核心',
    x: 266,
    y: 380,
    color: '#a478ff',
    note: '降低冲突强度，促成中立化或退出。',
  },
]

const HOW_TO_READ = [
  ['EchoBox', '回音壁容器，边框厚度与光晕代表讨论边界强度。'],
  ['Small balls', '人群簇，不代表真实个体或个人画像。'],
  ['Influence cores', '观念、内容、媒体、官方说明或梗化核心，不是人群球。'],
  ['Color change', '公开表达状态迁移：同化、中立化、退出或反噬。'],
  ['Fade out', '退出当前事件讨论，不代表问题已经解决。'],
]

function seededRandom(seed) {
  let value = seed % 2147483647
  if (value <= 0) value += 2147483646
  return () => {
    value = (value * 16807) % 2147483647
    return (value - 1) / 2147483646
  }
}

function createParticles(seed = 20260613) {
  const random = seededRandom(seed)
  const stateBuckets = ['support', 'neutral', 'oppose', 'uncertain', 'bridge']
  return Array.from({ length: PARTICLE_COUNT }, (_, index) => {
    const roll = random()
    const state =
      roll < 0.18
        ? stateBuckets[0]
        : roll < 0.46
          ? stateBuckets[1]
          : roll < 0.72
            ? stateBuckets[2]
            : roll < 0.9
              ? stateBuckets[3]
              : stateBuckets[4]
    const influenceWeight = 0.35 + random() * 0.95
    const activityWeight = 0.35 + random() * 0.9
    return {
      id: `cluster_${index}`,
      x: 52 + random() * (BOX_WIDTH - 104),
      y: 50 + random() * (BOX_HEIGHT - 100),
      vx: (random() - 0.5) * 0.72,
      vy: (random() - 0.5) * 0.72,
      radius: 2.7 + influenceWeight * 3.7,
      state,
      baseState: state,
      influenceWeight,
      activityWeight,
      fatigue: random() * 0.28,
      intensity: 0.26 + random() * 0.7,
      phase: random() * Math.PI * 2,
    }
  })
}

function scenarioTargetForParticle(particle, scenario) {
  const pull = scenario.pull
  if (particle.state === 'oppose') {
    if (pull.deconstruct > 0.3) return CORE_NODES[3]
    if (pull.official > pull.opposition) return CORE_NODES[1]
    if (pull.thirdParty > 0.28) return CORE_NODES[2]
    return CORE_NODES[0]
  }
  if (particle.state === 'support') return CORE_NODES[1]
  if (particle.state === 'bridge') return pull.deconstruct > 0.25 ? CORE_NODES[3] : CORE_NODES[2]
  if (particle.state === 'uncertain') return pull.thirdParty > pull.official ? CORE_NODES[2] : CORE_NODES[1]
  if (particle.state === 'withdrawn') return null
  return scenario.neutralization > 0.35 ? CORE_NODES[2] : CORE_NODES[3]
}

function mutateParticleState(particle, scenario, tick) {
  if (particle.state === 'withdrawn') return
  const gate = Math.abs(Math.sin((tick + particle.phase * 100 + particle.id.length) * 0.013))
  if (particle.state === 'oppose' && scenario.neutralization > 0.28 && gate > 0.996) {
    particle.state = scenario.deconstruction > 0.35 ? 'neutral' : 'uncertain'
    particle.intensity *= 0.72
  } else if (particle.state === 'uncertain' && scenario.neutralization > 0.32 && gate > 0.994) {
    particle.state = 'neutral'
    particle.intensity *= 0.82
  } else if (particle.state === 'neutral' && scenario.pull.official > 0.34 && gate > 0.997) {
    particle.state = 'support'
  } else if (particle.state === 'support' && scenario.breakout > 0.45 && gate > 0.998) {
    particle.state = 'uncertain'
  }

  particle.fatigue = Math.min(1, particle.fatigue + scenario.fatigue * 0.0009)
  particle.intensity = Math.min(1, Math.max(0.12, particle.intensity + scenario.hardening * 0.0007 - scenario.deconstruction * 0.0006))

  if (particle.fatigue > 0.86 && gate > 0.992) {
    particle.state = 'withdrawn'
    particle.intensity *= 0.42
  }
}

function drawRoundedRect(ctx, x, y, width, height, radius) {
  ctx.beginPath()
  ctx.moveTo(x + radius, y)
  ctx.arcTo(x + width, y, x + width, y + height, radius)
  ctx.arcTo(x + width, y + height, x, y + height, radius)
  ctx.arcTo(x, y + height, x, y, radius)
  ctx.arcTo(x, y, x + width, y, radius)
  ctx.closePath()
}

function drawCore(ctx, core, activeStrength) {
  const size = 20 + activeStrength * 18
  ctx.save()
  ctx.translate(core.x, core.y)
  ctx.shadowColor = core.color
  ctx.shadowBlur = 20 + activeStrength * 18
  ctx.fillStyle = `${core.color}32`
  ctx.strokeStyle = core.color
  ctx.lineWidth = 1.6
  ctx.beginPath()
  for (let i = 0; i < 6; i += 1) {
    const angle = Math.PI / 6 + (i * Math.PI * 2) / 6
    const px = Math.cos(angle) * size
    const py = Math.sin(angle) * size
    if (i === 0) ctx.moveTo(px, py)
    else ctx.lineTo(px, py)
  }
  ctx.closePath()
  ctx.fill()
  ctx.stroke()
  ctx.shadowBlur = 0
  ctx.fillStyle = '#eef4ff'
  ctx.font = '600 12px "Microsoft YaHei", sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText(core.label, 0, size + 17)
  ctx.restore()
}

function drawSandbox(ctx, particles, scenario, tick) {
  ctx.clearRect(0, 0, BOX_WIDTH, BOX_HEIGHT)

  ctx.save()
  const echo = scenario.echoStrength
  const gradient = ctx.createRadialGradient(BOX_WIDTH * 0.5, BOX_HEIGHT * 0.42, 20, BOX_WIDTH * 0.5, BOX_HEIGHT * 0.48, 480)
  gradient.addColorStop(0, 'rgba(66, 245, 215, 0.12)')
  gradient.addColorStop(0.55, 'rgba(120, 166, 255, 0.06)')
  gradient.addColorStop(1, 'rgba(255, 93, 143, 0.06)')
  ctx.fillStyle = gradient
  drawRoundedRect(ctx, 12, 12, BOX_WIDTH - 24, BOX_HEIGHT - 24, 22)
  ctx.fill()

  ctx.strokeStyle = `rgba(66, 245, 215, ${0.28 + echo * 0.54})`
  ctx.lineWidth = 2 + echo * 5
  ctx.shadowColor = '#42f5d7'
  ctx.shadowBlur = 10 + echo * 28
  drawRoundedRect(ctx, 12, 12, BOX_WIDTH - 24, BOX_HEIGHT - 24, 22)
  ctx.stroke()
  ctx.restore()

  ctx.save()
  ctx.strokeStyle = 'rgba(154, 166, 191, 0.08)'
  ctx.lineWidth = 1
  for (let x = 36; x < BOX_WIDTH; x += 36) {
    ctx.beginPath()
    ctx.moveTo(x, 24)
    ctx.lineTo(x, BOX_HEIGHT - 24)
    ctx.stroke()
  }
  for (let y = 36; y < BOX_HEIGHT; y += 36) {
    ctx.beginPath()
    ctx.moveTo(24, y)
    ctx.lineTo(BOX_WIDTH - 24, y)
    ctx.stroke()
  }
  ctx.restore()

  const activeCoreStrength = {
    opposition: scenario.pull.opposition,
    official: scenario.pull.official,
    thirdParty: scenario.pull.thirdParty,
    deconstruct: scenario.pull.deconstruct,
  }

  ctx.save()
  particles
    .filter((particle) => particle.state === 'bridge' && particle.id.endsWith('7'))
    .slice(0, 18)
    .forEach((particle) => {
      const target = scenarioTargetForParticle(particle, scenario) || CORE_NODES[2]
      ctx.strokeStyle = 'rgba(164, 120, 255, 0.18)'
      ctx.lineWidth = 0.8
      ctx.beginPath()
      ctx.moveTo(particle.x, particle.y)
      ctx.lineTo(target.x, target.y)
      ctx.stroke()
    })
  ctx.restore()

  CORE_NODES.forEach((core) => {
    drawCore(ctx, core, activeCoreStrength[core.id] || 0.08)
  })

  particles.forEach((particle) => {
    const opacity = particle.state === 'withdrawn' ? 0.18 : Math.max(0.22, 1 - particle.fatigue * 0.7)
    const color = STATE_COLORS[particle.state] || STATE_COLORS.neutral
    const pulse = 1 + Math.sin(tick * 0.04 + particle.phase) * 0.08 * particle.intensity
    const radius = particle.radius * pulse
    ctx.save()
    ctx.globalAlpha = opacity
    ctx.shadowColor = color
    ctx.shadowBlur = 3 + particle.intensity * 9
    ctx.fillStyle = color
    ctx.beginPath()
    ctx.arc(particle.x, particle.y, radius, 0, Math.PI * 2)
    ctx.fill()
    ctx.globalAlpha = Math.min(0.9, opacity + 0.12)
    ctx.strokeStyle = 'rgba(244, 247, 251, 0.22)'
    ctx.lineWidth = 0.7
    ctx.stroke()
    ctx.restore()
  })
}

function stepParticles(particles, scenario, tick) {
  particles.forEach((particle) => {
    mutateParticleState(particle, scenario, tick)
    if (particle.state === 'withdrawn') {
      particle.vx *= 0.985
      particle.vy *= 0.985
    }
    const target = scenarioTargetForParticle(particle, scenario)
    if (target) {
      const dx = target.x - particle.x
      const dy = target.y - particle.y
      const distance = Math.max(24, Math.hypot(dx, dy))
      const pullScale =
        ((target.id === 'opposition' ? scenario.pull.opposition : 0) +
          (target.id === 'official' ? scenario.pull.official : 0) +
          (target.id === 'thirdParty' ? scenario.pull.thirdParty : 0) +
          (target.id === 'deconstruct' ? scenario.pull.deconstruct : 0) +
          0.05) *
        0.004
      particle.vx += (dx / distance) * pullScale
      particle.vy += (dy / distance) * pullScale
    }
    particle.vx += Math.sin(tick * 0.015 + particle.phase) * 0.0022
    particle.vy += Math.cos(tick * 0.012 + particle.phase) * 0.002
    const maxSpeed = 0.24 + particle.activityWeight * 0.62
    const speed = Math.hypot(particle.vx, particle.vy)
    if (speed > maxSpeed) {
      particle.vx = (particle.vx / speed) * maxSpeed
      particle.vy = (particle.vy / speed) * maxSpeed
    }
    particle.x += particle.vx
    particle.y += particle.vy
    if (particle.x < 28 || particle.x > BOX_WIDTH - 28) {
      particle.vx *= -0.9
      particle.x = Math.min(BOX_WIDTH - 28, Math.max(28, particle.x))
    }
    if (particle.y < 28 || particle.y > BOX_HEIGHT - 28) {
      particle.vy *= -0.9
      particle.y = Math.min(BOX_HEIGHT - 28, Math.max(28, particle.y))
    }
    particle.vx *= 0.992
    particle.vy *= 0.992
  })
}

function buildMetrics(particles, scenario) {
  const counts = particles.reduce(
    (acc, particle) => {
      acc[particle.state] = (acc[particle.state] || 0) + 1
      return acc
    },
    { support: 0, neutral: 0, oppose: 0, uncertain: 0, bridge: 0, withdrawn: 0 },
  )
  const activeCount = Math.max(1, particles.length - counts.withdrawn)
  const intensity =
    particles.reduce((sum, particle) => sum + (particle.state === 'withdrawn' ? 0 : particle.intensity), 0) / activeCount
  const opposeShare = counts.oppose / particles.length
  const neutralShare = (counts.neutral + counts.uncertain) / particles.length
  return {
    counts,
    withdrawnShare: counts.withdrawn / particles.length,
    dormantGrievanceRisk: Math.min(1, scenario.hardening * 0.7 + opposeShare * 0.65 + counts.withdrawn / particles.length * 0.22),
    echoBoxSaturation: Math.min(1, scenario.echoStrength * 0.62 + intensity * 0.38),
    breakoutRisk: Math.min(1, scenario.breakout * 0.68 + opposeShare * 0.44),
    deconstructionWindow: Math.min(1, scenario.deconstruction * 0.72 + neutralShare * 0.28),
    responseTempo: scenario.tempo,
  }
}

function percent(value) {
  return Math.round(value * 100)
}

function MetricProgress({ label, value, strokeColor }) {
  return (
    <div className="ecosystem-progress-row">
      <Text>{label}</Text>
      <Progress percent={percent(value)} size="small" strokeColor={strokeColor} trailColor="rgba(154,166,191,0.18)" />
    </div>
  )
}

export function OpinionEcosystemSandbox() {
  const canvasRef = useRef(null)
  const particlesRef = useRef(createParticles())
  const frameRef = useRef(null)
  const tickRef = useRef(0)
  const scenarioRef = useRef(SCENARIOS.natural)
  const [scenarioKey, setScenarioKey] = useState('natural')
  const [playing, setPlaying] = useState(true)
  const [metrics, setMetrics] = useState(() => buildMetrics(particlesRef.current, SCENARIOS.natural))

  const scenario = SCENARIOS[scenarioKey] || SCENARIOS.natural

  useEffect(() => {
    scenarioRef.current = scenario
  }, [scenario])

  const drawCurrentFrame = useCallback(() => {
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
    context.setTransform(ratio, 0, 0, ratio, 0, 0)
    drawSandbox(context, particlesRef.current, scenarioRef.current, tickRef.current)
  }, [])

  useEffect(() => {
    let lastMetricTick = 0
    const animate = () => {
      if (playing) {
        tickRef.current += 1
        stepParticles(particlesRef.current, scenarioRef.current, tickRef.current)
      }
      drawCurrentFrame()
      if (tickRef.current - lastMetricTick > 18 || !playing) {
        lastMetricTick = tickRef.current
        setMetrics(buildMetrics(particlesRef.current, scenarioRef.current))
      }
      frameRef.current = requestAnimationFrame(animate)
    }
    frameRef.current = requestAnimationFrame(animate)
    return () => {
      if (frameRef.current) cancelAnimationFrame(frameRef.current)
    }
  }, [drawCurrentFrame, playing])

  const handleReset = useCallback(() => {
    particlesRef.current = createParticles()
    tickRef.current = 0
    setMetrics(buildMetrics(particlesRef.current, scenarioRef.current))
    drawCurrentFrame()
  }, [drawCurrentFrame])

  const distributionItems = useMemo(
    () => [
      { key: 'support', label: '正方核心 / 温和支持', value: metrics.counts.support, color: STATE_COLORS.support },
      { key: 'neutral', label: '中立围观 / 中立参与', value: metrics.counts.neutral, color: STATE_COLORS.neutral },
      { key: 'uncertain', label: '摇摆观望', value: metrics.counts.uncertain, color: STATE_COLORS.uncertain },
      { key: 'oppose', label: '温和反对 / 反方核心 / 极端反对', value: metrics.counts.oppose, color: STATE_COLORS.oppose },
      { key: 'bridge', label: '桥接 / 高影响人群簇', value: metrics.counts.bridge, color: STATE_COLORS.bridge },
      { key: 'withdrawn', label: '退出当前讨论', value: metrics.counts.withdrawn, color: STATE_COLORS.withdrawn },
    ],
    [metrics],
  )

  return (
    <div className="page-stack opinion-ecosystem-page">
      <div className="page-heading">
        <div>
          <Title level={2}>Opinion Ecosystem Sandbox / 舆论生态沙盒</Title>
          <Paragraph>
            前端-only mock visual prototype，用静态模拟数据展示 EchoBox、人群簇、影响核心与解构核心之间的公开表达状态迁移。
          </Paragraph>
        </div>
        <Space wrap>
          <Tag color="cyan">Mock visual prototype</Tag>
          <Tag color="blue">基于静态模拟数据</Tag>
          <Tag color="default">不代表全网全量覆盖</Tag>
          <Tag color="purple">不执行真实平台动作</Tag>
        </Space>
      </div>

      <Alert
        type="info"
        showIcon
        message="安全边界"
        description="本页面不连接后端 API、不读取 Evidence 数据、不调用真实平台或 LLM 服务、不抓取 URL。所有运动、权重、同化 / 中立化 / 退出 / 反噬 / 解构 / 处理节奏均为本地 mock 演示，不代表因果确定。"
      />

      <Card className="panel-card ecosystem-control-card">
        <Space size={12} wrap>
          <Segmented options={SCENARIO_OPTIONS} value={scenarioKey} onChange={setScenarioKey} />
          <Button
            icon={playing ? <PauseCircle size={16} /> : <PlayCircle size={16} />}
            onClick={() => setPlaying((value) => !value)}
            type="primary"
          >
            {playing ? 'Pause' : 'Play'}
          </Button>
          <Button icon={<RotateCcw size={16} />} onClick={handleReset}>
            Reset
          </Button>
          <Tag color="geekblue">当前场景：{scenario.label}</Tag>
          <Tag color="gold">处理节奏：{scenario.tempo}</Tag>
        </Space>
      </Card>

      <Row gutter={[16, 16]}>
        <Col span={16}>
          <Card
            className="panel-card ecosystem-canvas-card"
            title={
              <Space>
                <ScanLine size={18} />
                <span>EchoBox / 回音壁容器</span>
              </Space>
            }
            extra={<Tag color="cyan">border glow = echo chamber strength</Tag>}
          >
            <div
              className="ecosystem-canvas-shell"
              style={{
                '--echo-alpha': `${0.22 + scenario.echoStrength * 0.55}`,
                '--echo-blur': `${12 + scenario.echoStrength * 34}px`,
              }}
            >
              <canvas ref={canvasRef} aria-label="Mock Opinion Ecosystem Sandbox visualization" />
            </div>
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card ecosystem-side-card" title="Mock Metrics">
            <div className="ecosystem-stat-grid">
              <Statistic title="withdrawn share" value={percent(metrics.withdrawnShare)} suffix="%" />
              <Statistic title="echo box saturation" value={percent(metrics.echoBoxSaturation)} suffix="%" />
              <Statistic title="breakout risk" value={percent(metrics.breakoutRisk)} suffix="%" />
              <Statistic title="deconstruction window" value={percent(metrics.deconstructionWindow)} suffix="%" />
            </div>
            <MetricProgress label="dormant grievance risk" value={metrics.dormantGrievanceRisk} strokeColor="#ff5d8f" />
            <MetricProgress label="echo box saturation" value={metrics.echoBoxSaturation} strokeColor="#42f5d7" />
            <MetricProgress label="breakout risk" value={metrics.breakoutRisk} strokeColor="#f5c44b" />
            <MetricProgress label="deconstruction window score" value={metrics.deconstructionWindow} strokeColor="#a478ff" />
            <div className="ecosystem-recommendation">
              <Text type="secondary">Mock recommendation</Text>
              <Paragraph>{scenario.recommendation}</Paragraph>
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={8}>
          <Card className="panel-card" title="人群簇分布">
            <List
              dataSource={distributionItems}
              renderItem={(item) => (
                <List.Item>
                  <div className="ecosystem-distribution-row">
                    <Space>
                      <span className="ecosystem-dot" style={{ background: item.color }} />
                      <Text>{item.label}</Text>
                    </Space>
                    <Tag color="default">{item.value}</Tag>
                  </div>
                </List.Item>
              )}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card" title="Influence Cores / 影响核心">
            <List
              dataSource={CORE_NODES}
              renderItem={(core) => (
                <List.Item>
                  <div className="ecosystem-core-card">
                    <Space>
                      <span className="ecosystem-core-swatch" style={{ borderColor: core.color, boxShadow: `0 0 18px ${core.color}44` }} />
                      <div>
                        <Text strong>{core.label}</Text>
                        <div>
                          <Tag color="default">{core.type}</Tag>
                        </div>
                      </div>
                    </Space>
                    <Paragraph>{core.note}</Paragraph>
                  </div>
                </List.Item>
              )}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card" title="How to read this">
            <List
              dataSource={HOW_TO_READ}
              renderItem={([label, description]) => (
                <List.Item>
                  <div className="ecosystem-reading-row">
                    <Text strong>{label}</Text>
                    <Paragraph>{description}</Paragraph>
                  </div>
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>

      <Card
        className="panel-card ecosystem-boundary-card"
        title={
          <Space>
            <Sparkles size={18} />
            <span>Prototype boundary</span>
          </Space>
        }
      >
        <Space wrap>
          <Tag color="cyan">基于静态模拟数据</Tag>
          <Tag color="default">不代表全网全量覆盖</Tag>
          <Tag color="default">不代表因果确定</Tag>
          <Tag color="default">不执行真实平台动作</Tag>
          <Tag color="default">不连接 Evidence 数据</Tag>
          <Tag color="default">不调用真实 LLM</Tag>
        </Space>
      </Card>
    </div>
  )
}
