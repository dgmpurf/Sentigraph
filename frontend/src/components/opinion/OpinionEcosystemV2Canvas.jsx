import { Card, Col, Progress, Row, Space, Statistic, Tag, Timeline, Tooltip, Typography } from 'antd'
import { Activity, Boxes, CircleDot, Clock3, Compass, RadioTower, Sparkles } from 'lucide-react'
import { useEffect, useMemo, useRef } from 'react'

import { BOX_HEIGHT, BOX_WIDTH, campStateToVisual, scoreToPercent } from '../../data/opinionEcosystemMock.js'

const { Paragraph, Text } = Typography

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
  { key: 'natural', label: '自然演化', coreId: 'opposition' },
  { key: 'official_clarification', label: '官方澄清', coreId: 'official' },
  { key: 'faq_explainer', label: 'FAQ / 长文解释', coreId: 'third_party' },
  { key: 'third_party_explanation', label: '第三方说明', coreId: 'third_party' },
  { key: 'community_deconstruction', label: '社区解构', coreId: 'deconstruction' },
  { key: 'delayed_response', label: '延迟回应', coreId: 'opposition' },
  { key: 'no_response', label: '无回应', coreId: 'opposition' },
]

const CORE_ROLES = {
  opposition: {
    shortLabel: '反弹',
    roleLabel: 'Community backlash core',
    readableName: '社区反弹 / 高情绪叙事核心',
    marker: '!',
    anchor: { x: 42, y: 78, align: 'left' },
  },
  official: {
    shortLabel: '官方',
    roleLabel: 'Official statement core',
    readableName: '官方澄清 / 事实边界核心',
    marker: '□',
    anchor: { x: 570, y: 78, align: 'right' },
  },
  third_party: {
    shortLabel: '解释',
    roleLabel: 'Third-party explanation core',
    readableName: 'FAQ / 第三方解释核心',
    marker: '◇',
    anchor: { x: 570, y: 442, align: 'right' },
  },
  deconstruction: {
    shortLabel: '解构',
    roleLabel: 'Meme / deconstruction core',
    readableName: '社区解构 / meme 降压核心',
    marker: '✦',
    anchor: { x: 42, y: 442, align: 'left' },
  },
}

const DYNAMICS_LABELS = [
  ['同化', 'soft clusters moving toward a stronger narrative core'],
  ['中立化', 'opposed or supportive clusters cooling toward gray/yellow'],
  ['退出', 'fatigued clusters fading toward the boundary'],
  ['固化', 'high-identity clusters locking around a core'],
  ['反噬', 'poor timing increasing hardening or opposition pull'],
  ['再激活', 'dormant grievance reappearing after a shock event'],
]

const SCENARIO_VISUALS = {
  natural: {
    label: 'baseline ecology',
    redDim: 0,
    neutralBoost: 0,
    bridgeBoost: 0,
    withdrawBoost: 0,
    breakoutGlow: 0.12,
    coreBoost: {},
    tone: '#42f5d7',
  },
  official_clarification: {
    label: 'official core stronger; opposition glow cools',
    redDim: 0.24,
    neutralBoost: 0.18,
    bridgeBoost: 0.06,
    withdrawBoost: 0,
    breakoutGlow: 0.04,
    coreBoost: { official: 0.44 },
    tone: '#42f5d7',
  },
  faq_explainer: {
    label: 'explanation core stabilizes neutral clusters',
    redDim: 0.18,
    neutralBoost: 0.26,
    bridgeBoost: 0.12,
    withdrawBoost: 0.04,
    breakoutGlow: 0.02,
    coreBoost: { third_party: 0.44, official: 0.16 },
    tone: '#78a6ff',
  },
  third_party_explanation: {
    label: 'bridge clusters become visible',
    redDim: 0.12,
    neutralBoost: 0.12,
    bridgeBoost: 0.38,
    withdrawBoost: 0,
    breakoutGlow: 0.04,
    coreBoost: { third_party: 0.52 },
    tone: '#a478ff',
  },
  community_deconstruction: {
    label: 'deconstruction core grows; hot clusters cool',
    redDim: 0.28,
    neutralBoost: 0.16,
    bridgeBoost: 0.28,
    withdrawBoost: 0.18,
    breakoutGlow: 0,
    coreBoost: { deconstruction: 0.62 },
    tone: '#a478ff',
  },
  delayed_response: {
    label: 'latent backlash and dormant risk increase',
    redDim: -0.12,
    neutralBoost: 0,
    bridgeBoost: 0,
    withdrawBoost: 0.02,
    breakoutGlow: 0.32,
    coreBoost: { opposition: 0.36 },
    tone: '#ff5d8f',
  },
  no_response: {
    label: 'saturation and breakout risk increase',
    redDim: -0.2,
    neutralBoost: 0,
    bridgeBoost: 0,
    withdrawBoost: 0,
    breakoutGlow: 0.48,
    coreBoost: { opposition: 0.54 },
    tone: '#ff5d8f',
  },
}

function getCoreRoleKey(core) {
  if (CORE_ROLES[core.core_id]) return core.core_id
  const haystack = `${core.core_id || ''} ${core.core_type || ''} ${core.source_type || ''} ${core.label || ''}`.toLowerCase()
  if (haystack.includes('official') || haystack.includes('statement')) return 'official'
  if (haystack.includes('meme') || haystack.includes('deconstruction') || haystack.includes('reframe')) return 'deconstruction'
  if (haystack.includes('third') || haystack.includes('explanation') || haystack.includes('media') || haystack.includes('analysis')) return 'third_party'
  if (haystack.includes('forum') || haystack.includes('thread') || Number(core.stance_score) < -0.25) return 'opposition'
  return 'third_party'
}

function getCoreRole(core) {
  return CORE_ROLES[getCoreRoleKey(core)] || CORE_ROLES.third_party
}

function selectDisplayCores(cores) {
  const order = ['opposition', 'official', 'third_party', 'deconstruction']
  const selected = new Map()
  cores.forEach((core) => {
    const roleKey = getCoreRoleKey(core)
    const previous = selected.get(roleKey)
    if (!previous || Number(core.gravitational_pull || 0) > Number(previous.gravitational_pull || 0)) {
      selected.set(roleKey, core)
    }
  })
  return order
    .map((roleKey) => {
      const core = selected.get(roleKey)
      if (!core) return null
      const role = CORE_ROLES[roleKey]
      return {
        ...core,
        core_id: roleKey,
        label: role.shortLabel,
        role_key: roleKey,
        visual_color:
          roleKey === 'opposition'
            ? '#ff5d8f'
            : roleKey === 'official'
              ? '#42f5d7'
              : roleKey === 'deconstruction'
                ? '#a478ff'
                : '#78a6ff',
        position:
          roleKey === 'opposition'
            ? { x: 206, y: 170 }
            : roleKey === 'official'
              ? { x: 576, y: 164 }
              : roleKey === 'third_party'
                ? { x: 532, y: 378 }
                : { x: 232, y: 378 },
      }
    })
    .filter(Boolean)
}

function drawRoundedRect(ctx, x, y, width, height, radius) {
  ctx.beginPath()
  ctx.moveTo(x + radius, y)
  ctx.arcTo(x + width, y, x + width, y + height, radius)
  ctx.arcTo(x + width, y + height, x, y + height, radius)
  ctx.arcTo(x, y + height, x, y, radius)
  ctx.arcTo(x, y, x + radius, y, radius)
  ctx.closePath()
}

function drawEchoBoundary(ctx, scenario, tick, scenarioVisual) {
  const echo = scenario.echoBox.echo_chamber_score
  const breakout = scenario.echoBox.breakout_risk + scenarioVisual.breakoutGlow
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
  gradient.addColorStop(1, `rgba(255, 93, 143, ${0.04 + breakout * 0.1})`)
  ctx.fillStyle = gradient
  drawRoundedRect(ctx, inset, inset, width, height, 26)
  ctx.fill()

  ctx.shadowColor = scenarioVisual.tone
  ctx.shadowBlur = 14 + breakout * 34
  ctx.strokeStyle = `rgba(66, 245, 215, ${0.34 + echo * 0.45})`
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

  ctx.strokeStyle = `rgba(255, 93, 143, ${0.12 + breakout * 0.38})`
  ctx.lineWidth = 1.4
  for (let i = 0; i < 6; i += 1) {
    const crackX = inset + 42 + i * 116
    const crackY = inset + 8 + Math.sin(tick * 0.02 + i) * 10
    ctx.beginPath()
    ctx.moveTo(crackX, crackY)
    ctx.lineTo(crackX + 16, crackY + 18 + breakout * 16)
    ctx.lineTo(crackX + 8, crackY + 42)
    ctx.stroke()
  }

  ctx.fillStyle = '#dffbf7'
  ctx.font = '700 13px "Microsoft YaHei", sans-serif'
  ctx.fillText('EchoBox / discussion boundary', inset + 16, inset + 28)
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

function drawCoreShape(ctx, size, coreId) {
  if (coreId === 'official') {
    ctx.beginPath()
    ctx.rect(-size, -size, size * 2, size * 2)
    return
  }
  if (coreId === 'deconstruction') {
    ctx.beginPath()
    for (let i = 0; i < 10; i += 1) {
      const angle = -Math.PI / 2 + (i * Math.PI * 2) / 10
      const radius = i % 2 === 0 ? size * 1.18 : size * 0.66
      const x = Math.cos(angle) * radius
      const y = Math.sin(angle) * radius
      if (i === 0) ctx.moveTo(x, y)
      else ctx.lineTo(x, y)
    }
    ctx.closePath()
    return
  }
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

function drawCoreCallout(ctx, core, role, size) {
  const anchor = role.anchor
  const boxWidth = 145
  const boxHeight = 38
  const boxX = anchor.align === 'right' ? anchor.x - boxWidth : anchor.x
  const boxY = anchor.y
  const midX = boxX + (anchor.align === 'right' ? boxWidth : 0)
  const midY = boxY + boxHeight / 2

  ctx.save()
  ctx.strokeStyle = `${core.visual_color}66`
  ctx.lineWidth = 1
  ctx.beginPath()
  ctx.moveTo(core.position.x, core.position.y + size * 0.55)
  ctx.lineTo(midX, midY)
  ctx.stroke()

  ctx.fillStyle = 'rgba(8, 12, 20, 0.82)'
  ctx.strokeStyle = `${core.visual_color}88`
  drawRoundedRect(ctx, boxX, boxY, boxWidth, boxHeight, 8)
  ctx.fill()
  ctx.stroke()

  ctx.fillStyle = '#f4f7fb'
  ctx.font = '700 12px "Microsoft YaHei", sans-serif'
  ctx.textAlign = anchor.align
  ctx.fillText(role.readableName, anchor.align === 'right' ? boxX + boxWidth - 10 : boxX + 10, boxY + 17, boxWidth - 20)
  ctx.fillStyle = 'rgba(214, 222, 239, 0.72)'
  ctx.font = '10px "Microsoft YaHei", sans-serif'
  ctx.fillText(role.roleLabel, anchor.align === 'right' ? boxX + boxWidth - 10 : boxX + 10, boxY + 31, boxWidth - 20)
  ctx.restore()
}

function drawCore(ctx, core, scenario, tick, scenarioVisual) {
  const role = getCoreRole(core)
  const pull = Math.min(1, core.gravitational_pull + (scenarioVisual.coreBoost[core.core_id] || 0))
  const aura = 42 + pull * 118 + Math.sin(tick * 0.03 + core.core_id.length) * pull * 8
  const size = 18 + pull * 29

  ctx.save()
  ctx.translate(core.position.x, core.position.y)
  ctx.strokeStyle = `${core.visual_color}46`
  ctx.fillStyle = `${core.visual_color}0d`
  ctx.lineWidth = 1.15
  ctx.beginPath()
  ctx.arc(0, 0, aura, 0, Math.PI * 2)
  ctx.fill()
  ctx.stroke()

  ctx.beginPath()
  ctx.arc(0, 0, aura * 0.62, 0, Math.PI * 2)
  ctx.strokeStyle = `${core.visual_color}26`
  ctx.stroke()

  ctx.shadowColor = core.visual_color
  ctx.shadowBlur = 20 + pull * 32
  ctx.fillStyle = `${core.visual_color}34`
  ctx.strokeStyle = core.visual_color
  ctx.lineWidth = 2.4
  drawCoreShape(ctx, size, core.core_id)
  ctx.fill()
  ctx.stroke()

  ctx.shadowBlur = 0
  ctx.fillStyle = '#f4f7fb'
  ctx.font = '800 12px "Microsoft YaHei", sans-serif'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'
  ctx.fillText(role.shortLabel, 0, 0, size * 1.45)

  ctx.fillStyle = core.core_id === 'deconstruction' ? '#f5c44b' : 'rgba(244, 247, 251, 0.74)'
  ctx.font = '900 13px "Microsoft YaHei", sans-serif'
  ctx.fillText(role.marker, 0, -size - 12)

  ctx.strokeStyle = `rgba(244, 247, 251, ${0.22 + pull * 0.48})`
  ctx.lineWidth = 1
  ctx.beginPath()
  ctx.arc(0, 0, size + 8, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * Math.min(1, pull))
  ctx.stroke()

  if (scenario.scenarioKey === 'community_deconstruction' && core.core_id === 'deconstruction') {
    ctx.fillStyle = '#f5c44b'
    ctx.font = '700 10px "Microsoft YaHei", sans-serif'
    ctx.fillText('meme / reframe', 0, size + 17)
  }
  ctx.restore()

  drawCoreCallout(ctx, core, role, size)
}

function drawPeopleCluster(ctx, cluster, scenario, tick, scenarioVisual) {
  const visual = campStateToVisual(cluster.camp_state, cluster)
  const isWithdrawn = cluster.camp_state === 'withdrawn'
  const isDormant = cluster.camp_state === 'dormant_grievance'
  const isOppose = visual.key === 'oppose'
  const isBridge = visual.key === 'bridge'
  const isNeutralLike = visual.key === 'neutral' || visual.key === 'uncertain'
  const fatigueOpacity = Math.max(0.2, 1 - cluster.fatigue * 0.74)
  const scenarioOpacity =
    (isOppose ? -scenarioVisual.redDim : 0) +
    (isNeutralLike ? scenarioVisual.neutralBoost * 0.24 : 0) +
    (isBridge ? scenarioVisual.bridgeBoost * 0.28 : 0) -
    (isWithdrawn ? scenarioVisual.withdrawBoost * 0.16 : 0)
  const opacity = isWithdrawn ? 0.13 + scenarioVisual.withdrawBoost * 0.1 : Math.max(0.2, Math.min(1, fatigueOpacity + scenarioOpacity))
  const highEmotionBoost = 1 + cluster.expression_intensity * 0.18
  const pulse = 1 + Math.sin(tick * (0.036 + cluster.activity_weight * 0.018) + cluster.phase) * 0.09 * highEmotionBoost
  const bridgeRadiusBoost = isBridge ? 1 + scenarioVisual.bridgeBoost * 0.32 : 1
  const radius = (2.5 + cluster.population_weight * 3.7 + cluster.influence_weight * 1.8) * pulse * bridgeRadiusBoost
  const outlineColor = isDormant ? '#1b1020' : isBridge ? '#d9c6ff' : 'rgba(244, 247, 251, 0.24)'

  ctx.save()
  ctx.globalAlpha = opacity
  ctx.shadowColor = visual.color
  ctx.shadowBlur = 3 + cluster.expression_intensity * 8 + (isBridge ? scenarioVisual.bridgeBoost * 8 : 0)
  ctx.fillStyle = visual.color
  ctx.beginPath()
  ctx.arc(cluster.position.x, cluster.position.y, radius, 0, Math.PI * 2)
  ctx.fill()
  ctx.shadowBlur = 0
  ctx.globalAlpha = Math.min(0.92, opacity + 0.16)
  ctx.strokeStyle = outlineColor
  ctx.lineWidth = isDormant ? 2 : isBridge ? 1.5 : 0.75
  ctx.stroke()

  const satelliteCount = cluster.population_weight > 0.72 ? 2 : cluster.population_weight > 0.46 ? 1 : 0
  for (let i = 0; i < satelliteCount; i += 1) {
    const angle = cluster.phase + tick * (0.012 + i * 0.004) + i * Math.PI
    const orbit = radius + 4 + i * 2
    ctx.globalAlpha = opacity * 0.52
    ctx.beginPath()
    ctx.arc(cluster.position.x + Math.cos(angle) * orbit, cluster.position.y + Math.sin(angle) * orbit, Math.max(1.2, radius * 0.28), 0, Math.PI * 2)
    ctx.fill()
  }
  ctx.restore()
}

function drawBridgeLinks(ctx, scenario, peopleClusters, scenarioVisual) {
  const displayCores = selectDisplayCores(scenario.influenceCores)
  const cores = new Map(displayCores.map((core) => [core.core_id, core]))
  const maxLinks = 22 + Math.round(scenarioVisual.bridgeBoost * 22)
  ctx.save()
  peopleClusters
    .filter((cluster) => cluster.bridge_power > 0.68 && cluster.camp_state !== 'withdrawn')
    .slice(0, maxLinks)
    .forEach((cluster, index) => {
      const target = cores.get(index % 2 === 0 ? 'third_party' : 'deconstruction') || scenario.influenceCores[0]
      if (!target) return
      ctx.strokeStyle = `rgba(164, 120, 255, ${0.18 + scenarioVisual.bridgeBoost * 0.18})`
      ctx.lineWidth = 0.8 + scenarioVisual.bridgeBoost * 0.35
      ctx.beginPath()
      ctx.moveTo(cluster.position.x, cluster.position.y)
      ctx.quadraticCurveTo(BOX_WIDTH / 2, BOX_HEIGHT / 2, target.position.x, target.position.y)
      ctx.stroke()
    })
  ctx.restore()
}

function drawEventTokenLink(ctx, scenarioKey, scenario, tick, scenarioVisual) {
  const activeToken = EVENT_TOKENS.find((token) => token.key === scenarioKey) || EVENT_TOKENS[0]
  const target = selectDisplayCores(scenario.influenceCores).find((core) => core.core_id === activeToken.coreId)
  if (!target) return
  const progress = (Math.sin(tick * 0.035) + 1) / 2
  const start = { x: BOX_WIDTH - 66, y: 40 }
  const x = start.x + (target.position.x - start.x) * progress
  const y = start.y + (target.position.y - start.y) * progress

  ctx.save()
  ctx.strokeStyle = `${scenarioVisual.tone}7a`
  ctx.setLineDash([7, 7])
  ctx.lineWidth = 1.4
  ctx.beginPath()
  ctx.moveTo(start.x, start.y)
  ctx.lineTo(target.position.x, target.position.y)
  ctx.stroke()
  ctx.setLineDash([])
  ctx.fillStyle = scenarioVisual.tone
  ctx.shadowColor = scenarioVisual.tone
  ctx.shadowBlur = 16
  ctx.beginPath()
  ctx.arc(x, y, 5.5, 0, Math.PI * 2)
  ctx.fill()
  ctx.restore()
}

function drawBreakoutSignals(ctx, scenario, tick, scenarioVisual) {
  const intensity = scenario.echoBox.breakout_risk + scenarioVisual.breakoutGlow
  if (intensity < 0.34) return
  ctx.save()
  ctx.fillStyle = `rgba(255, 93, 143, ${0.2 + intensity * 0.22})`
  ctx.strokeStyle = `rgba(255, 93, 143, ${0.2 + intensity * 0.25})`
  for (let i = 0; i < 12; i += 1) {
    const angle = (i / 12) * Math.PI * 2 + tick * 0.008
    const x = BOX_WIDTH / 2 + Math.cos(angle) * (BOX_WIDTH * 0.43 + Math.sin(tick * 0.02 + i) * 8)
    const y = BOX_HEIGHT / 2 + Math.sin(angle) * (BOX_HEIGHT * 0.4 + Math.cos(tick * 0.018 + i) * 6)
    ctx.beginPath()
    ctx.arc(x, y, 2.4 + intensity * 2.2, 0, Math.PI * 2)
    ctx.fill()
  }
  ctx.restore()
}

function drawV2Sandbox(ctx, scenario, peopleClusters, tick) {
  const scenarioVisual = SCENARIO_VISUALS[scenario.scenarioKey] || SCENARIO_VISUALS.natural
  const displayCores = selectDisplayCores(scenario.influenceCores)
  ctx.clearRect(0, 0, BOX_WIDTH, BOX_HEIGHT)
  drawEchoBoundary(ctx, scenario, tick, scenarioVisual)
  drawGrid(ctx)
  drawBreakoutSignals(ctx, scenario, tick, scenarioVisual)
  drawEventTokenLink(ctx, scenario.scenarioKey, scenario, tick, scenarioVisual)
  drawBridgeLinks(ctx, scenario, peopleClusters, scenarioVisual)
  peopleClusters.forEach((cluster) => drawPeopleCluster(ctx, cluster, scenario, tick, scenarioVisual))
  displayCores.forEach((core) => drawCore(ctx, core, scenario, tick, scenarioVisual))
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
        <Tooltip
          key={token.key}
          title="Local mock scenario token only; it does not call external APIs or fetch URLs."
          placement="top"
        >
          <span className={token.key === scenarioKey ? 'active' : ''}>{token.label}</span>
        </Tooltip>
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

function CoreLegend({ scenarioView }) {
  const scenarioVisual = SCENARIO_VISUALS[scenarioView.scenarioKey] || SCENARIO_VISUALS.natural
  return (
    <div className="ecosystem-v2-core-legend">
      {scenarioView.influenceCores.map((core, index) => {
        const roleKey = getCoreRoleKey(core)
        const role = getCoreRole(core)
        const boostedPull = Math.min(1, core.gravitational_pull + (scenarioVisual.coreBoost[roleKey] || 0))
        return (
          <div key={`${core.core_id}-${core.label}-${index}`} className="ecosystem-v2-core-legend-item">
            <span style={{ borderColor: core.visual_color, boxShadow: `0 0 18px ${core.visual_color}55` }}>{role.marker}</span>
            <div>
              <Text strong>{role.readableName || core.label}</Text>
              <Paragraph>{role.roleLabel} · pull {scoreToPercent(boostedPull)}%</Paragraph>
            </div>
          </div>
        )
      })}
    </div>
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
  const scenarioVisual = SCENARIO_VISUALS[scenarioView.scenarioKey] || SCENARIO_VISUALS.natural

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
                <Tag color="gold">mock event token</Tag>
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
              <Statistic title="匿名簇数量" value={peopleClusters.length} suffix="簇" />
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
              <Tag color="default">{scenarioVisual.label}</Tag>
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
          <Card className="panel-card ecosystem-v2-card" title="InfluenceCore legend / 核心说明">
            <CoreLegend scenarioView={scenarioView} />
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
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Card className="panel-card ecosystem-v2-card ecosystem-v2-read-card" title="How to read V2 / 快速阅读">
            <div className="ecosystem-v2-read-grid">
              <Space>
                <CircleDot size={15} />
                <Text>小球是匿名 PeopleCluster，不是真实个人。</Text>
              </Space>
              <Space>
                <RadioTower size={15} />
                <Text>大节点是 InfluenceCore，代表内容、叙事、官方、媒体或 meme 核心。</Text>
              </Space>
              <Space>
                <Compass size={15} />
                <Text>边界越厚表示 EchoBox 越强；缺口表示可渗透。</Text>
              </Space>
              <Space>
                <Clock3 size={15} />
                <Text>时间轴展示本地 mock 响应节奏，不代表因果证明。</Text>
              </Space>
              <Space>
                <Activity size={15} />
                <Text>指标用于辅助解释，不代表全网或全平台覆盖。</Text>
              </Space>
            </div>
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
          <Tag>selected public sample where applicable</Tag>
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
