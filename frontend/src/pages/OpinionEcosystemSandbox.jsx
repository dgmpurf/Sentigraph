import { Alert, Button, Card, Col, List, Progress, Row, Segmented, Space, Statistic, Tag, Typography } from 'antd'
import { PauseCircle, PlayCircle, RotateCcw, ScanLine, Sparkles } from 'lucide-react'
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'

import {
  BOX_HEIGHT,
  BOX_WIDTH,
  HOW_TO_READ,
  OPINION_ECOSYSTEM_SCHEMA_STATUS,
  OPINION_STATE_COLORS,
  OPINION_STATE_LABELS,
  SCENARIO_OPTIONS,
  applyMockScenario,
  campStateToVisual,
  computeCampDistribution,
  computeMockMetrics,
  createOpinionEcosystemMock,
  scoreToPercent,
  scenarioTargetForCluster,
  stepPeopleClusters,
} from '../data/opinionEcosystemMock.js'

const { Paragraph, Text, Title } = Typography

function drawRoundedRect(ctx, x, y, width, height, radius) {
  ctx.beginPath()
  ctx.moveTo(x + radius, y)
  ctx.arcTo(x + width, y, x + width, y + height, radius)
  ctx.arcTo(x + width, y + height, x, y + height, radius)
  ctx.arcTo(x, y + height, x, y, radius)
  ctx.arcTo(x, y, x + radius, y, radius)
  ctx.closePath()
}

function drawCore(ctx, core) {
  const size = 20 + core.gravitational_pull * 18
  ctx.save()
  ctx.translate(core.position.x, core.position.y)
  ctx.shadowColor = core.visual_color
  ctx.shadowBlur = 20 + core.gravitational_pull * 18
  ctx.fillStyle = `${core.visual_color}32`
  ctx.strokeStyle = core.visual_color
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

function drawSandbox(ctx, peopleClusters, scenario, tick) {
  ctx.clearRect(0, 0, BOX_WIDTH, BOX_HEIGHT)

  ctx.save()
  const echo = scenario.echoBox.echo_chamber_score
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

  ctx.save()
  peopleClusters
    .filter((cluster) => cluster.bridge_power > 0.74 && cluster.cluster_id.endsWith('7'))
    .slice(0, 18)
    .forEach((cluster) => {
      const target = scenarioTargetForCluster(cluster, scenario)
      if (!target) return
      ctx.strokeStyle = 'rgba(164, 120, 255, 0.18)'
      ctx.lineWidth = 0.8
      ctx.beginPath()
      ctx.moveTo(cluster.position.x, cluster.position.y)
      ctx.lineTo(target.position.x, target.position.y)
      ctx.stroke()
    })
  ctx.restore()

  scenario.influenceCores.forEach((core) => drawCore(ctx, core))

  peopleClusters.forEach((cluster) => {
    const visual = campStateToVisual(cluster.camp_state, cluster)
    const opacity = cluster.camp_state === 'withdrawn' ? 0.18 : Math.max(0.22, 1 - cluster.fatigue * 0.7)
    const pulse = 1 + Math.sin(tick * 0.04 + cluster.phase) * 0.08 * cluster.expression_intensity
    const radius = (2.7 + cluster.influence_weight * 3.7) * pulse
    ctx.save()
    ctx.globalAlpha = opacity
    ctx.shadowColor = visual.color
    ctx.shadowBlur = 3 + cluster.expression_intensity * 9
    ctx.fillStyle = visual.color
    ctx.beginPath()
    ctx.arc(cluster.position.x, cluster.position.y, radius, 0, Math.PI * 2)
    ctx.fill()
    ctx.globalAlpha = Math.min(0.9, opacity + 0.12)
    ctx.strokeStyle = 'rgba(244, 247, 251, 0.22)'
    ctx.lineWidth = 0.7
    ctx.stroke()
    ctx.restore()
  })
}

function MetricProgress({ label, value, strokeColor }) {
  return (
    <div className="ecosystem-progress-row">
      <Text>{label}</Text>
      <Progress percent={scoreToPercent(value)} size="small" strokeColor={strokeColor} trailColor="rgba(154,166,191,0.18)" />
    </div>
  )
}

function createScenarioView(baseModel, scenarioKey, peopleClusters) {
  const scenario = applyMockScenario(baseModel, scenarioKey)
  return { ...scenario, peopleClusters }
}

export function OpinionEcosystemSandbox() {
  const canvasRef = useRef(null)
  const baseModelRef = useRef(null)
  const peopleClustersRef = useRef(null)
  const frameRef = useRef(null)
  const tickRef = useRef(0)
  const scenarioRef = useRef(null)
  const [scenarioKey, setScenarioKey] = useState('natural')
  const [playing, setPlaying] = useState(true)

  if (!baseModelRef.current) {
    baseModelRef.current = createOpinionEcosystemMock()
    peopleClustersRef.current = baseModelRef.current.peopleClusters
    scenarioRef.current = createScenarioView(baseModelRef.current, scenarioKey, peopleClustersRef.current)
  }

  const scenario = useMemo(
    () => createScenarioView(baseModelRef.current, scenarioKey, peopleClustersRef.current),
    [scenarioKey],
  )

  const [metrics, setMetrics] = useState(() =>
    computeMockMetrics(
      scenarioRef.current.echoBox,
      scenarioRef.current.influenceCores,
      peopleClustersRef.current,
      scenarioRef.current.responseTempo,
      scenarioRef.current.reputationMemory,
    ),
  )

  useEffect(() => {
    scenarioRef.current = createScenarioView(baseModelRef.current, scenarioKey, peopleClustersRef.current)
    setMetrics(
      computeMockMetrics(
        scenarioRef.current.echoBox,
        scenarioRef.current.influenceCores,
        peopleClustersRef.current,
        scenarioRef.current.responseTempo,
        scenarioRef.current.reputationMemory,
      ),
    )
  }, [scenarioKey])

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
    drawSandbox(context, peopleClustersRef.current, scenarioRef.current, tickRef.current)
  }, [])

  useEffect(() => {
    let lastMetricTick = 0
    const animate = () => {
      if (playing) {
        tickRef.current += 1
        stepPeopleClusters(peopleClustersRef.current, scenarioRef.current, tickRef.current)
      }
      drawCurrentFrame()
      if (tickRef.current - lastMetricTick > 18 || !playing) {
        lastMetricTick = tickRef.current
        setMetrics(
          computeMockMetrics(
            scenarioRef.current.echoBox,
            scenarioRef.current.influenceCores,
            peopleClustersRef.current,
            scenarioRef.current.responseTempo,
            scenarioRef.current.reputationMemory,
          ),
        )
      }
      frameRef.current = requestAnimationFrame(animate)
    }
    frameRef.current = requestAnimationFrame(animate)
    return () => {
      if (frameRef.current) cancelAnimationFrame(frameRef.current)
    }
  }, [drawCurrentFrame, playing])

  const handleReset = useCallback(() => {
    baseModelRef.current = createOpinionEcosystemMock()
    peopleClustersRef.current = baseModelRef.current.peopleClusters
    scenarioRef.current = createScenarioView(baseModelRef.current, scenarioKey, peopleClustersRef.current)
    tickRef.current = 0
    setMetrics(
      computeMockMetrics(
        scenarioRef.current.echoBox,
        scenarioRef.current.influenceCores,
        peopleClustersRef.current,
        scenarioRef.current.responseTempo,
        scenarioRef.current.reputationMemory,
      ),
    )
    drawCurrentFrame()
  }, [drawCurrentFrame, scenarioKey])

  const distributionItems = useMemo(() => {
    const distribution = computeCampDistribution(peopleClustersRef.current)
    return [
      { key: 'support', label: '正方核心 / 温和支持', value: distribution.visualCounts.support, color: OPINION_STATE_COLORS.support },
      { key: 'neutral', label: OPINION_STATE_LABELS.neutral, value: distribution.visualCounts.neutral, color: OPINION_STATE_COLORS.neutral },
      { key: 'uncertain', label: OPINION_STATE_LABELS.uncertain, value: distribution.visualCounts.uncertain, color: OPINION_STATE_COLORS.uncertain },
      { key: 'oppose', label: '温和反对 / 反方核心 / 高强度反对', value: distribution.visualCounts.oppose, color: OPINION_STATE_COLORS.oppose },
      { key: 'bridge', label: OPINION_STATE_LABELS.bridge, value: distribution.visualCounts.bridge, color: OPINION_STATE_COLORS.bridge },
      { key: 'withdrawn', label: OPINION_STATE_LABELS.withdrawn, value: distribution.visualCounts.withdrawn, color: OPINION_STATE_COLORS.withdrawn },
    ]
  }, [metrics])

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
          <Tag color="geekblue">当前场景：{scenario.scenarioLabel}</Tag>
          <Tag color="gold">处理节奏：{scenario.responseTempo.recommendation_label}</Tag>
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
                '--echo-alpha': `${0.22 + scenario.echoBox.echo_chamber_score * 0.55}`,
                '--echo-blur': `${12 + scenario.echoBox.echo_chamber_score * 34}px`,
              }}
            >
              <canvas ref={canvasRef} aria-label="Mock Opinion Ecosystem Sandbox visualization" />
            </div>
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card ecosystem-side-card" title="Mock Metrics">
            <div className="ecosystem-stat-grid">
              <Statistic title="withdrawn share" value={scoreToPercent(metrics.withdrawnShare)} suffix="%" />
              <Statistic title="echo box saturation" value={scoreToPercent(metrics.echoBoxSaturation)} suffix="%" />
              <Statistic title="breakout risk" value={scoreToPercent(metrics.breakoutRisk)} suffix="%" />
              <Statistic title="deconstruction window" value={scoreToPercent(metrics.deconstructionWindow)} suffix="%" />
            </div>
            <MetricProgress label="dormant grievance risk" value={metrics.dormantGrievanceRisk} strokeColor="#ff5d8f" />
            <MetricProgress label="echo box saturation" value={metrics.echoBoxSaturation} strokeColor="#42f5d7" />
            <MetricProgress label="breakout risk" value={metrics.breakoutRisk} strokeColor="#f5c44b" />
            <MetricProgress label="deconstruction window score" value={metrics.deconstructionWindow} strokeColor="#a478ff" />
            <div className="ecosystem-recommendation">
              <Text type="secondary">Mock recommendation</Text>
              <Paragraph>{scenario.responseTempo.recommendation_text}</Paragraph>
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={6}>
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
        <Col span={6}>
          <Card className="panel-card" title="Influence Cores / 影响核心">
            <List
              dataSource={scenario.influenceCores}
              renderItem={(core) => (
                <List.Item>
                  <div className="ecosystem-core-card">
                    <Space>
                      <span
                        className="ecosystem-core-swatch"
                        style={{ borderColor: core.visual_color, boxShadow: `0 0 18px ${core.visual_color}44` }}
                      />
                      <div>
                        <Text strong>{core.label}</Text>
                        <div>
                          <Tag color="default">{core.core_type}</Tag>
                        </div>
                      </div>
                    </Space>
                    <Paragraph>
                      pull {scoreToPercent(core.gravitational_pull)}% · bridge {scoreToPercent(core.bridge_power)}% · evidence{' '}
                      {scoreToPercent(core.evidence_strength)}%
                    </Paragraph>
                  </div>
                </List.Item>
              )}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="panel-card" title="模型对象 / Schema status">
            <List
              dataSource={OPINION_ECOSYSTEM_SCHEMA_STATUS}
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
        <Col span={6}>
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

      <Row gutter={[16, 16]}>
        <Col span={8}>
          <Card className="panel-card" title="CampDynamics / mock 转移规则">
            <MetricProgress label="neutralization score" value={scenario.campDynamics.neutralization_score} strokeColor="#42f5d7" />
            <MetricProgress label="withdrawal score" value={scenario.campDynamics.withdrawal_score} strokeColor="#667085" />
            <MetricProgress label="backlash score" value={scenario.campDynamics.backlash_score} strokeColor="#ff5d8f" />
            <MetricProgress label="reactivation risk" value={scenario.campDynamics.reactivation_risk} strokeColor="#f5c44b" />
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card" title="DeconstructionCore / 解构核心">
            <MetricProgress label="neutralization power" value={scenario.deconstructionCore.neutralization_power} strokeColor="#42f5d7" />
            <MetricProgress label="withdrawal power" value={scenario.deconstructionCore.withdrawal_power} strokeColor="#667085" />
            <MetricProgress label="fit score" value={scenario.deconstructionCore.deconstruction_fit_score} strokeColor="#a478ff" />
            <Paragraph>{scenario.deconstructionCore.label} 仅为本地 mock 节点，不代表真实平台内容。</Paragraph>
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card" title="ReputationMemory / 长期残留">
            <MetricProgress
              label="unresolved grievance score"
              value={scenario.reputationMemory.unresolved_grievance_score}
              strokeColor="#ff5d8f"
            />
            <MetricProgress label="trust recovery" value={scenario.reputationMemory.trust_recovery} strokeColor="#54f5a8" />
            <MetricProgress label="reactivation risk" value={scenario.reputationMemory.reactivation_risk} strokeColor="#f5c44b" />
            <Paragraph>退出讨论不等于问题解决；该卡片只提示 mock 风险记忆，不做真实性判断。</Paragraph>
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
