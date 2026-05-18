import {
  Alert,
  Button,
  Card,
  Col,
  Empty,
  Input,
  InputNumber,
  List,
  Row,
  Select,
  Segmented,
  Skeleton,
  Space,
  Statistic,
  Tag,
  Typography,
} from 'antd'
import {
  Activity,
  Copy,
  Download,
  FileText,
  Gauge,
  GitBranch,
  PlayCircle,
  RadioTower,
  RefreshCw,
  RotateCcw,
  ShieldCheck,
  StepForward,
  Waves,
} from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'

import {
  exportSimulationStrategyMarkdownReport,
  getSimulationDemoScenario,
  getSimulationEthicsPolicy,
  initializeCaseSimulation,
  previewCaseSimulationInitialization,
  runSimulation,
} from '../api/sentigraphApi.js'

const { Paragraph, Text, Title } = Typography

const BASE_ALLOWED_INTERVENTIONS = [
  {
    value: 'clarification',
    label: '事实澄清',
    message: '发布已核实事实、调查范围和下一次更新时间。',
    framing: 'clarifying',
    source_credibility: 0.78,
    stance_direction: 0.36,
    emotional_intensity: 0.22,
    evidence_strength: 0.68,
    platform_reach: 0.6,
    intensity: 0.62,
  },
  {
    value: 'apology',
    label: '公开致歉',
    message: '承认影响、表达歉意，并说明后续纠正动作。',
    framing: 'accountability',
    source_credibility: 0.76,
    stance_direction: 0.42,
    emotional_intensity: 0.34,
    evidence_strength: 0.58,
    platform_reach: 0.62,
    intensity: 0.66,
  },
  {
    value: 'compensation',
    label: '补偿方案',
    message: '说明透明、可核验的补偿或修复路径。',
    framing: 'remediation',
    source_credibility: 0.74,
    stance_direction: 0.48,
    emotional_intensity: 0.28,
    evidence_strength: 0.72,
    platform_reach: 0.58,
    intensity: 0.68,
  },
  {
    value: 'faq',
    label: 'FAQ 问答',
    message: '集中回答高频事实问题，减少误解和重复争议。',
    framing: 'faq',
    source_credibility: 0.7,
    stance_direction: 0.3,
    emotional_intensity: 0.18,
    evidence_strength: 0.62,
    platform_reach: 0.52,
    intensity: 0.54,
  },
  {
    value: 'progress_update',
    label: '进展更新',
    message: '公开调查进展、已完成事项和下一步时间表。',
    framing: 'progress',
    source_credibility: 0.72,
    stance_direction: 0.34,
    emotional_intensity: 0.2,
    evidence_strength: 0.64,
    platform_reach: 0.56,
    intensity: 0.58,
  },
  {
    value: 'third_party_evidence',
    label: '第三方证据',
    message: '引用可核验第三方证据，辅助解释事实边界。',
    framing: 'evidence',
    source_credibility: 0.86,
    stance_direction: 0.38,
    emotional_intensity: 0.2,
    evidence_strength: 0.86,
    platform_reach: 0.6,
    intensity: 0.64,
  },
  {
    value: 'misinformation_correction',
    label: '误信息纠正',
    message: '用冷静事实纠正未经证实的说法，并提供验证路径。',
    framing: 'correction',
    source_credibility: 0.8,
    stance_direction: 0.34,
    emotional_intensity: 0.2,
    evidence_strength: 0.82,
    platform_reach: 0.62,
    intensity: 0.66,
  },
  {
    value: 'no_response',
    label: '不回应基线',
    message: '不发布公开回应，用作透明基线对照。',
    framing: 'no_response',
    source_credibility: 0,
    stance_direction: 0,
    emotional_intensity: 0,
    evidence_strength: 0,
    platform_reach: 0,
    intensity: 0,
  },
]

const OPTIONAL_MODERATION_INTERVENTIONS = [
  {
    value: 'content_removal_with_explanation',
    label: '透明说明后内容移除',
    message: '模拟平台授权、规则清晰且配套公开说明的内容移除风险收益。',
    framing: 'content_removal_with_explanation',
    source_credibility: 0.8,
    stance_direction: 0.2,
    emotional_intensity: 0.18,
    evidence_strength: 0.76,
    platform_reach: 0.42,
    intensity: 0.72,
  },
  {
    value: 'visibility_reduction',
    label: '合规可见性降低',
    message: '模拟平台授权的可见性降低，并估计曝光降低、反弹和外溢风险。',
    framing: 'visibility_reduction',
    source_credibility: 0.74,
    stance_direction: 0.12,
    emotional_intensity: 0.16,
    evidence_strength: 0.66,
    platform_reach: 0.34,
    intensity: 0.62,
  },
  {
    value: 'platform_labeling',
    label: '平台标注',
    message: '模拟以标注和规则说明替代直接删除的低反弹治理方案。',
    framing: 'platform_labeling',
    source_credibility: 0.78,
    stance_direction: 0.18,
    emotional_intensity: 0.14,
    evidence_strength: 0.72,
    platform_reach: 0.3,
    intensity: 0.5,
  },
]

const FORBIDDEN_INTERVENTIONS = new Set([
  'fake_consensus',
  'bot_amplification',
  'fake_event',
  'deceptive_distraction',
  'covert_influencer_seeding',
  'targeted_persuasion',
  'suppression',
  'illegal_suppression',
  'covert_censorship',
  'covert_suppression',
  'targeted_silencing',
  'platform_governance_evasion',
])

const VISIBILITY_INTERVENTIONS = new Set([
  'content_removal_with_explanation',
  'visibility_reduction',
  'platform_labeling',
])

const COMMUNITY_REGIONS = {
  opposition: {
    label: '核心反对者',
    x: 18,
    y: 58,
    width: 30,
    height: 52,
    tone: 'red',
  },
  neutral: {
    label: '中立观察者',
    x: 48,
    y: 55,
    width: 32,
    height: 50,
    tone: 'default',
  },
  support: {
    label: '支持者',
    x: 78,
    y: 58,
    width: 28,
    height: 48,
    tone: 'green',
  },
  authority: {
    label: '权威/媒体影响区',
    x: 52,
    y: 18,
    width: 38,
    height: 28,
    tone: 'cyan',
  },
  bridge: {
    label: '跨圈层桥接节点',
    x: 52,
    y: 78,
    width: 30,
    height: 24,
    tone: 'geekblue',
  },
}

const interventionLabelMap = Object.fromEntries(
  [...BASE_ALLOWED_INTERVENTIONS, ...OPTIONAL_MODERATION_INTERVENTIONS].map((item) => [item.value, item.label]),
)

function safeText(value, fallback = '-') {
  if (value === null || value === undefined || value === '') return fallback
  return String(value)
}

function formatNumber(value, digits = 2) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue.toFixed(digits) : '0.00'
}

function formatPercent(value) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? `${Math.round(numericValue * 100)}%` : '0%'
}

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value))
}

function getErrorMessage(error, fallback) {
  const detail = error?.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (detail && typeof detail === 'object' && !Array.isArray(detail)) {
    return detail.message || detail.error || fallback
  }
  if (Array.isArray(detail) && detail.length) {
    return detail.map((item) => item?.msg || 'validation error').join('; ')
  }
  return error?.message || fallback
}

function getInterventionDefinition(type) {
  return (
    BASE_ALLOWED_INTERVENTIONS.find((item) => item.value === type) ||
    OPTIONAL_MODERATION_INTERVENTIONS.find((item) => item.value === type) ||
    BASE_ALLOWED_INTERVENTIONS[0]
  )
}

function getOpinionTone(opinion, metrics, agent) {
  if (metrics?.polarization_index > 0.34 && agent?.attention_budget > 0.7) return 'volatile'
  if (opinion < -0.22) return 'negative'
  if (opinion > 0.22) return 'positive'
  return 'neutral'
}

function getBubbleColors(tone) {
  const colors = {
    negative: { background: 'rgba(255, 93, 143, 0.76)', border: 'rgba(255, 93, 143, 0.95)' },
    neutral: { background: 'rgba(154, 166, 191, 0.5)', border: 'rgba(202, 211, 229, 0.72)' },
    positive: { background: 'rgba(66, 245, 215, 0.68)', border: 'rgba(66, 245, 215, 0.94)' },
    volatile: { background: 'rgba(255, 161, 67, 0.72)', border: 'rgba(255, 190, 105, 0.98)' },
  }
  return colors[tone] || colors.neutral
}

function classifyCommunity(agent) {
  const text = `${agent?.community_id || ''} ${agent?.identity_group || ''}`.toLowerCase()
  if (text.includes('bridge')) return 'bridge'
  if (text.includes('official') || text.includes('media') || text.includes('authority')) return 'authority'
  if (text.includes('support') || text.includes('evidence')) return 'support'
  if (
    text.includes('opposition') ||
    text.includes('critic') ||
    text.includes('concern') ||
    text.includes('affected') ||
    text.includes('rumor')
  ) {
    return 'opposition'
  }
  return 'neutral'
}

function hashAgentId(value) {
  return String(value || '')
    .split('')
    .reduce((sum, char) => sum + char.charCodeAt(0), 0)
}

function buildCentralityMap(edges = []) {
  const centrality = new Map()
  for (const edge of edges) {
    const source = edge.source_agent_id
    const target = edge.target_agent_id
    if (source) {
      const current = centrality.get(source) || { count: 0, bridge: 0 }
      centrality.set(source, { count: current.count + 1, bridge: Math.max(current.bridge, edge.bridge_score || 0) })
    }
    if (target) {
      const current = centrality.get(target) || { count: 0, bridge: 0 }
      centrality.set(target, { count: current.count + 1, bridge: Math.max(current.bridge, edge.bridge_score || 0) })
    }
  }
  return centrality
}

function deriveInitialMetrics(agents = []) {
  if (!agents.length) {
    return {
      average_latent_opinion: 0,
      average_expressed_opinion: 0,
      negative_ratio: 0,
      neutral_ratio: 1,
      positive_ratio: 0,
      polarization_index: 0,
      attention_level: 0,
      trust_recovery_proxy: 0,
      intervention_effect_score: 0,
      ethical_risk_flags: [],
    }
  }
  const averageExpressed = agents.reduce((sum, agent) => sum + agent.expressed_opinion, 0) / agents.length
  const averageLatent = agents.reduce((sum, agent) => sum + agent.latent_opinion, 0) / agents.length
  const negativeRatio = agents.filter((agent) => agent.expressed_opinion < -0.15).length / agents.length
  const positiveRatio = agents.filter((agent) => agent.expressed_opinion > 0.15).length / agents.length
  const attentionLevel = agents.reduce((sum, agent) => sum + agent.attention_budget, 0) / agents.length
  const polarizationIndex =
    agents.reduce((sum, agent) => sum + Math.abs(agent.expressed_opinion - averageExpressed), 0) / agents.length
  return {
    average_latent_opinion: averageLatent,
    average_expressed_opinion: averageExpressed,
    negative_ratio: negativeRatio,
    neutral_ratio: Math.max(0, 1 - negativeRatio - positiveRatio),
    positive_ratio: positiveRatio,
    polarization_index: polarizationIndex,
    attention_level: attentionLevel,
    trust_recovery_proxy: clamp((averageLatent + 1) / 2, 0, 1),
    intervention_effect_score: 0,
    ethical_risk_flags: [],
  }
}

function buildVisibilityIntervention(type) {
  if (!VISIBILITY_INTERVENTIONS.has(type)) return null
  const defaults = {
    content_removal_with_explanation: {
      target_message_reach: 0.94,
      current_visibility: 1,
      removal_time: 0.35,
      residual_copies: 0.22,
      screenshot_probability: 0.28,
      repost_migration_probability: 0.22,
      perceived_suppression: 0.28,
      policy_violation_clarity: 0.8,
      legitimacy_of_removal: 0.78,
      public_explanation_quality: 0.82,
      reactance_amplification: 0.32,
      martyr_effect: 0.2,
      cross_platform_spillover: 0.26,
      neutral_audience_negative_shift: 0.1,
      hard_opposition_negative_shift: 0.24,
    },
    visibility_reduction: {
      target_message_reach: 0.86,
      current_visibility: 1,
      removal_time: 0.28,
      residual_copies: 0.3,
      screenshot_probability: 0.24,
      repost_migration_probability: 0.18,
      perceived_suppression: 0.34,
      policy_violation_clarity: 0.68,
      legitimacy_of_removal: 0.64,
      public_explanation_quality: 0.62,
      reactance_amplification: 0.36,
      martyr_effect: 0.24,
      cross_platform_spillover: 0.24,
      neutral_audience_negative_shift: 0.13,
      hard_opposition_negative_shift: 0.27,
    },
    platform_labeling: {
      target_message_reach: 0.76,
      current_visibility: 1,
      removal_time: 0.18,
      residual_copies: 0.48,
      screenshot_probability: 0.16,
      repost_migration_probability: 0.12,
      perceived_suppression: 0.18,
      policy_violation_clarity: 0.72,
      legitimacy_of_removal: 0.76,
      public_explanation_quality: 0.78,
      reactance_amplification: 0.22,
      martyr_effect: 0.12,
      cross_platform_spillover: 0.14,
      neutral_audience_negative_shift: 0.06,
      hard_opposition_negative_shift: 0.14,
    },
  }
  return {
    intervention_type: type,
    ...(defaults[type] || defaults.content_removal_with_explanation),
    policy_basis: 'platform_policy',
    authorization_source: 'platform_policy',
    public_explanation_required: true,
  }
}

function buildIntervention(type, scenario) {
  const definition = getInterventionDefinition(type)
  return {
    intervention_id: `ui_intervention_${type}`,
    intervention_type: type,
    topic: scenario?.topic || 'brand_crisis',
    source_type: 'official',
    message: definition.message,
    target_scope: 'aggregate',
    publication_step: 1,
    source_credibility: definition.source_credibility ?? 0.75,
    stance_direction: definition.stance_direction ?? 0.35,
    emotional_intensity: definition.emotional_intensity ?? 0.24,
    evidence_strength: definition.evidence_strength ?? 0.65,
    framing: definition.framing || 'clarifying',
    responsibility_acknowledgement: type === 'apology' ? 0.72 : 0.42,
    transparency_level: type === 'no_response' ? 0 : 0.76,
    intensity: definition.intensity ?? 0.6,
    visibility_intervention: buildVisibilityIntervention(type),
  }
}

function buildScenarioForRun(scenario, interventionType, steps) {
  return {
    ...scenario,
    config: {
      ...(scenario?.config || {}),
      steps,
    },
    interventions: [buildIntervention(interventionType, scenario)],
  }
}

function getAllowedOptions(policy) {
  const policyAllowed = Array.isArray(policy?.allowed_intervention_types)
    ? new Set(policy.allowed_intervention_types)
    : new Set(BASE_ALLOWED_INTERVENTIONS.map((item) => item.value))
  const policyForbidden = Array.isArray(policy?.forbidden_intervention_types)
    ? new Set(policy.forbidden_intervention_types)
    : FORBIDDEN_INTERVENTIONS

  const baseOptions = BASE_ALLOWED_INTERVENTIONS.filter(
    (item) => policyAllowed.has(item.value) && !policyForbidden.has(item.value) && !FORBIDDEN_INTERVENTIONS.has(item.value),
  )
  const moderationOptions = OPTIONAL_MODERATION_INTERVENTIONS.filter(
    (item) => policyAllowed.has(item.value) && !policyForbidden.has(item.value) && !FORBIDDEN_INTERVENTIONS.has(item.value),
  )
  return [...baseOptions, ...moderationOptions].map((item) => ({
    label: item.label,
    value: item.value,
  }))
}

function getEventCards(scenario, selectedInterventionType) {
  const messageCards = (scenario?.messages || []).map((message) => ({
    key: message.message_id,
    label: message.source_type === 'public_posts' ? 'organic negative post' : safeText(message.source_type),
    source_type: message.source_type,
    intervention_type: 'organic_signal',
    source_credibility: message.source_credibility,
    emotional_intensity: message.emotional_intensity,
    evidence_strength: message.evidence_strength,
    platform_reach: message.platform_reach,
    active: false,
  }))
  const intervention = buildIntervention(selectedInterventionType, scenario)
  return [
    ...messageCards,
    {
      key: intervention.intervention_id,
      label: interventionLabelMap[selectedInterventionType] || selectedInterventionType,
      source_type: intervention.source_type,
      intervention_type: selectedInterventionType,
      source_credibility: intervention.source_credibility,
      emotional_intensity: intervention.emotional_intensity,
      evidence_strength: intervention.evidence_strength,
      platform_reach: getInterventionDefinition(selectedInterventionType).platform_reach ?? 0.56,
      active: true,
    },
  ]
}

function getTrendDisplay(trend) {
  const displays = {
    improving: { label: '风险下降', color: 'green' },
    worsening: { label: '风险上升', color: 'red' },
    stable: { label: '稳定', color: 'default' },
    unknown: { label: '未知', color: 'default' },
  }
  return displays[trend] || displays.unknown
}

function getFinalMetrics(result) {
  return result?.final_metrics || result?.step_results?.[result.step_results.length - 1]?.metrics || null
}

function computeRiskProxy(metrics) {
  if (!metrics) return null
  const rawScore =
    (metrics.negative_ratio ?? 0) * 52 +
    (metrics.polarization_index ?? 0) * 28 +
    (metrics.attention_level ?? 0) * 12 -
    (metrics.trust_recovery_proxy ?? 0) * 14
  return clamp(rawScore, 0, 100)
}

function computeBacklashRisk(metrics, interventionType) {
  if (!metrics) return null
  const isVisibilityAction = VISIBILITY_INTERVENTIONS.has(interventionType)
  const baseline = isVisibilityAction ? 0.18 : 0.06
  return clamp(
    baseline +
      (metrics.polarization_index ?? 0) * 0.46 +
      (metrics.attention_level ?? 0) * 0.22 -
      (metrics.trust_recovery_proxy ?? 0) * 0.12,
    0,
    1,
  )
}

function formatDelta(value, { percent = false, signed = true } = {}) {
  if (value === null || value === undefined || value === '') return '-'
  if (!Number.isFinite(Number(value))) return '-'
  const numericValue = Number(value)
  const prefix = signed && numericValue > 0 ? '+' : ''
  if (percent) return `${prefix}${Math.round(numericValue * 100)}%`
  return `${prefix}${numericValue.toFixed(2)}`
}

function getDeltaTone(value, lowerIsBetter = true) {
  if (value === null || value === undefined || value === '') return 'default'
  if (!Number.isFinite(Number(value)) || Math.abs(value) < 0.005) return 'default'
  const improved = lowerIsBetter ? value < 0 : value > 0
  return improved ? 'green' : 'red'
}

function buildComparisonSummary(resultA, resultB, interventionA, interventionB) {
  const metricsA = getFinalMetrics(resultA)
  const metricsB = getFinalMetrics(resultB)
  const riskA = computeRiskProxy(metricsA)
  const riskB = computeRiskProxy(metricsB)
  const riskDelta = riskA === null || riskB === null ? null : riskB - riskA
  const negativeRatioDelta = (metricsB?.negative_ratio ?? 0) - (metricsA?.negative_ratio ?? 0)
  const polarizationDelta = (metricsB?.polarization_index ?? 0) - (metricsA?.polarization_index ?? 0)
  const trustRecoveryDelta = (metricsB?.trust_recovery_proxy ?? 0) - (metricsA?.trust_recovery_proxy ?? 0)
  const attentionLevelDelta = (metricsB?.attention_level ?? 0) - (metricsA?.attention_level ?? 0)
  const backlashA = computeBacklashRisk(metricsA, interventionA)
  const backlashB = computeBacklashRisk(metricsB, interventionB)
  const backlashDelta = backlashA === null || backlashB === null ? null : backlashB - backlashA
  const visibilityA = resultA?.visibility_intervention_result || null
  const visibilityB = resultB?.visibility_intervention_result || null
  const visibilityDelta = (field) => {
    if (!visibilityA && !visibilityB) return null
    return (visibilityB?.[field] ?? 0) - (visibilityA?.[field] ?? 0)
  }
  const flags = [
    ...(metricsA?.ethical_risk_flags || []).map((flag) => `A: ${flag}`),
    ...(metricsB?.ethical_risk_flags || []).map((flag) => `B: ${flag}`),
    ...(visibilityA?.warnings || []).map((warning) => `A visibility: ${warning}`),
    ...(visibilityB?.warnings || []).map((warning) => `B visibility: ${warning}`),
  ]

  let betterOption = 'inconclusive'
  if (riskDelta !== null) {
    if (Math.abs(riskDelta) < 0.5) betterOption = 'tie'
    else betterOption = riskDelta < 0 ? 'B' : 'A'
  }

  return {
    better_option: betterOption,
    risk_a: riskA,
    risk_b: riskB,
    risk_delta: riskDelta,
    negative_ratio_delta: negativeRatioDelta,
    polarization_delta: polarizationDelta,
    trust_recovery_delta: trustRecoveryDelta,
    attention_level_delta: attentionLevelDelta,
    backlash_risk_a: backlashA,
    backlash_risk_b: backlashB,
    backlash_risk_delta: backlashDelta,
    visibility_a: visibilityA,
    visibility_b: visibilityB,
    exposure_reduction_delta: visibilityDelta('exposure_reduction'),
    visibility_backlash_delta: visibilityDelta('backlash_cost'),
    trust_loss_delta: visibilityDelta('trust_loss'),
    spillover_risk_delta: visibilityDelta('spillover_risk'),
    net_risk_change_delta: visibilityDelta('net_risk_change'),
    ethical_risk_notes: flags.length
      ? flags
      : ['No additional ethical risk flags were returned by the deterministic aggregate simulation.'],
    recommendation: 'human_review_required',
  }
}

function getCommunityLabel(key) {
  return COMMUNITY_REGIONS[key]?.label || key
}

function buildAgentVisuals(scenario, metrics, initialMetrics, stepResult) {
  const agents = scenario?.agents || []
  const centralityMap = buildCentralityMap(scenario?.network_edges || [])
  const baseAverage = initialMetrics?.average_expressed_opinion ?? deriveInitialMetrics(agents).average_expressed_opinion
  const aggregateDelta = (metrics?.average_expressed_opinion ?? baseAverage) - baseAverage

  return agents.map((agent, index) => {
    const communityKey = classifyCommunity(agent)
    const region = COMMUNITY_REGIONS[communityKey] || COMMUNITY_REGIONS.neutral
    const communityMetrics = stepResult?.community_metrics?.[agent.community_id]
    const communityDelta = communityMetrics
      ? communityMetrics.average_expressed_opinion - agent.expressed_opinion
      : aggregateDelta
    const expressedOpinion = clamp(
      agent.expressed_opinion + communityDelta * (1 - agent.stubbornness * 0.45),
      -1,
      1,
    )
    const hash = hashAgentId(agent.agent_id || index)
    const angle = ((hash % 360) * Math.PI) / 180
    const ring = 0.18 + ((hash % 37) / 100)
    const jitterX = Math.cos(angle) * region.width * ring
    const jitterY = Math.sin(angle) * region.height * ring
    const centrality = centralityMap.get(agent.agent_id) || { count: 1, bridge: 0 }
    const size = clamp(28 + centrality.count * 2.8 + centrality.bridge * 16, 28, 58)
    const attention = clamp((metrics?.attention_level ?? agent.attention_budget) * 0.48 + agent.attention_budget * 0.52, 0.24, 1)
    const tone = getOpinionTone(expressedOpinion, metrics, agent)
    const colors = getBubbleColors(tone)
    return {
      agent_id: agent.agent_id,
      community_id: agent.community_id,
      region: communityKey,
      expressedOpinion,
      latentOpinion: clamp(agent.latent_opinion + aggregateDelta * 0.45, -1, 1),
      attention,
      fatigue: agent.fatigue,
      size,
      tone,
      x: clamp(region.x + jitterX, 6, 94),
      y: clamp(region.y + jitterY, 10, 90),
      background: colors.background,
      border: colors.border,
      active: stepResult?.active_intervention_type && stepResult.active_intervention_type !== 'no_response',
    }
  })
}

function BubbleCanvas({
  compact = false,
  currentStepIndex,
  initialMetrics,
  metrics,
  scenario,
  stepResult,
  title = '舆情泡泡沙盘',
}) {
  const visuals = useMemo(
    () => buildAgentVisuals(scenario, metrics, initialMetrics, stepResult),
    [initialMetrics, metrics, scenario, stepResult],
  )

  if (!scenario?.agents?.length) {
    return (
      <Card className={`panel-card simulation-canvas-card ${compact ? 'simulation-canvas-compact' : ''}`}>
        <Empty description="请先加载安全演示场景" image={Empty.PRESENTED_IMAGE_SIMPLE} />
      </Card>
    )
  }

  return (
    <Card className={`panel-card simulation-canvas-card ${compact ? 'simulation-canvas-compact' : ''}`}>
      <div className="simulation-canvas-header">
        <Space>
          <Waves size={18} />
          <Title level={4}>{title}</Title>
        </Space>
        <Space wrap>
          <Tag color="cyan">deterministic</Tag>
          <Tag color="geekblue">aggregate only</Tag>
          <Tag color={stepResult ? 'green' : 'default'}>
            {stepResult ? `Step ${currentStepIndex + 1}` : '未运行'}
          </Tag>
        </Space>
      </div>

      <div className={`simulation-bubble-canvas ${compact ? 'simulation-bubble-canvas-compact' : ''}`}>
        {Object.entries(COMMUNITY_REGIONS).map(([key, region]) => (
          <div
            className={`simulation-community-region simulation-community-${key}`}
            key={key}
            style={{
              left: `${region.x}%`,
              top: `${region.y}%`,
              width: `${region.width}%`,
              height: `${region.height}%`,
            }}
          >
            <Tag color={region.tone}>{region.label}</Tag>
          </div>
        ))}

        {stepResult ? <div className="simulation-shockwave" key={`shockwave-${stepResult.step}`} /> : null}

        {visuals.map((agent) => (
          <div
            aria-label={`${agent.agent_id} ${getCommunityLabel(agent.region)}`}
            className={`simulation-bubble simulation-bubble-${agent.tone} ${agent.active ? 'simulation-bubble-active' : ''}`}
            key={agent.agent_id}
            role="img"
            style={{
              left: `calc(${agent.x}% - ${agent.size / 2}px)`,
              top: `calc(${agent.y}% - ${agent.size / 2}px)`,
              width: `${agent.size}px`,
              height: `${agent.size}px`,
              opacity: agent.attention,
              background: agent.background,
              borderColor: agent.border,
              boxShadow: agent.active
                ? `0 0 ${Math.round(agent.size * 0.7)}px ${agent.border}`
                : `0 0 ${Math.round(agent.size * 0.34)}px rgba(66, 245, 215, 0.12)`,
            }}
            title={`${agent.agent_id} | ${agent.community_id} | expressed ${formatNumber(agent.expressedOpinion)}`}
          >
            <span>{formatNumber(agent.expressedOpinion, 1)}</span>
          </div>
        ))}
      </div>
    </Card>
  )
}

function EventCards({ events = [], activeInterventionType }) {
  if (!events.length) {
    return <Empty description="暂无消息事件" image={Empty.PRESENTED_IMAGE_SIMPLE} />
  }
  return (
    <div className="simulation-event-strip">
      {events.map((event) => (
        <div
          className={`simulation-event-card ${event.intervention_type === activeInterventionType ? 'active' : ''}`}
          key={event.key}
        >
          <Space direction="vertical" size={7} className="full-width">
            <Space wrap>
              <Tag color={event.active ? 'cyan' : 'orange'}>{event.label}</Tag>
              <Tag>{event.source_type}</Tag>
              <Tag color="geekblue">{event.intervention_type}</Tag>
            </Space>
            <div className="simulation-event-metrics">
              <span>cred {formatPercent(event.source_credibility)}</span>
              <span>emo {formatPercent(event.emotional_intensity)}</span>
              <span>evd {formatPercent(event.evidence_strength)}</span>
              <span>reach {formatPercent(event.platform_reach)}</span>
            </div>
          </Space>
        </div>
      ))}
    </div>
  )
}

function MetricTile({ label, value, suffix, tone = 'cyan' }) {
  return (
    <div className="simulation-metric-tile">
      <Text type="secondary">{label}</Text>
      <Statistic value={value} precision={typeof value === 'number' ? 2 : undefined} suffix={suffix} />
      <Tag color={tone}>{label}</Tag>
    </div>
  )
}

function MetricsPanel({ metrics, result }) {
  const flags = metrics?.ethical_risk_flags || []
  return (
    <Card className="panel-card simulation-side-card">
      <div className="panel-heading">
        <Space>
          <Gauge size={18} />
          <Title level={4}>聚合指标</Title>
        </Space>
        <Tag color="cyan">MVP</Tag>
      </div>
      <div className="simulation-metric-grid">
        <MetricTile label="平均潜在态度" value={metrics?.average_latent_opinion ?? 0} />
        <MetricTile label="平均表达态度" value={metrics?.average_expressed_opinion ?? 0} />
        <MetricTile label="负向比例" value={Math.round((metrics?.negative_ratio ?? 0) * 100)} suffix="%" tone="red" />
        <MetricTile label="中立比例" value={Math.round((metrics?.neutral_ratio ?? 0) * 100)} suffix="%" tone="default" />
        <MetricTile label="正向比例" value={Math.round((metrics?.positive_ratio ?? 0) * 100)} suffix="%" tone="green" />
        <MetricTile label="极化指数" value={metrics?.polarization_index ?? 0} tone="orange" />
        <MetricTile label="注意力水平" value={Math.round((metrics?.attention_level ?? 0) * 100)} suffix="%" />
        <MetricTile label="信任恢复代理" value={Math.round((metrics?.trust_recovery_proxy ?? 0) * 100)} suffix="%" tone="green" />
        <MetricTile label="干预效果分" value={metrics?.intervention_effect_score ?? 0} tone="geekblue" />
      </div>

      <Card className="simulation-nested-card" title="伦理风险标记">
        {flags.length ? (
          <Space wrap>
            {flags.map((flag) => (
              <Tag color="orange" key={flag}>
                {flag}
              </Tag>
            ))}
          </Space>
        ) : (
          <Text type="secondary">暂无伦理风险标记</Text>
        )}
      </Card>

      {result?.warnings?.length ? (
        <Alert
          className="simulation-inline-alert"
          message="沙盘限制"
          description={result.warnings.join('；')}
          type="info"
          showIcon
        />
      ) : null}
    </Card>
  )
}

function ExplanationPanel({ metrics, result, selectedInterventionType, stepResult }) {
  const trend = getTrendDisplay(stepResult?.trend_direction || 'unknown')
  const communityEntries = Object.entries(stepResult?.community_metrics || {})
    .map(([community, communityMetrics]) => ({
      community,
      negative_ratio: communityMetrics.negative_ratio,
      polarization_index: communityMetrics.polarization_index,
    }))
    .sort((a, b) => b.negative_ratio - a.negative_ratio)
    .slice(0, 3)

  const risingReason =
    stepResult?.trend_direction === 'worsening'
      ? '负向表达或极化代理指标相对基线走高，需要关注高注意力群体的反应。'
      : metrics?.negative_ratio > 0.45
        ? '当前负向比例仍然偏高，若注意力继续集中，后续仍可能出现上行压力。'
        : '当前没有明显上行信号；仍需结合更多场景和监控快照复核。'
  const fallingReason =
    stepResult?.trend_direction === 'improving'
      ? safeText(stepResult?.forecast_reason, '负向表达相对基线下降，透明回应在当前假设下带来一定缓和。')
      : metrics?.trust_recovery_proxy > 0.55
        ? '信任恢复代理指标较好，说明当前回应在合成假设下有一定缓和空间。'
        : '当前下降信号有限，透明解释、证据强度和持续更新仍是主要观察点。'

  return (
    <Card className="panel-card simulation-side-card">
      <div className="panel-heading">
        <Space>
          <Activity size={18} />
          <Title level={4}>预测解释</Title>
        </Space>
        <Tag color={trend.color}>{trend.label}</Tag>
      </div>

      <Alert
        className="simulation-disclaimer-alert"
        message="当前只是确定性沙盘模拟，不代表真实未来必然发生。"
        type="info"
        showIcon
      />

      <div className="simulation-explanation-grid">
        <div>
          <Title level={5}>为什么风险上升</Title>
          <Paragraph>{risingReason}</Paragraph>
        </div>
        <div>
          <Title level={5}>为什么风险下降</Title>
          <Paragraph>{fallingReason}</Paragraph>
        </div>
        <div>
          <Title level={5}>主要驱动因素</Title>
          <Paragraph>
            负向比例 {formatPercent(metrics?.negative_ratio)}，极化指数 {formatNumber(metrics?.polarization_index)}，
            注意力水平 {formatPercent(metrics?.attention_level)}。
          </Paragraph>
        </div>
        <div>
          <Title level={5}>哪些群体受影响最大</Title>
          {communityEntries.length ? (
            <Space direction="vertical" size={6}>
              {communityEntries.map((item) => (
                <Tag color="orange" key={item.community}>
                  {item.community}: 负向 {formatPercent(item.negative_ratio)}
                </Tag>
              ))}
            </Space>
          ) : (
            <Text type="secondary">运行后展示社群层面的聚合变化。</Text>
          )}
        </div>
        <div>
          <Title level={5}>哪个干预正在生效</Title>
          <Paragraph>
            {interventionLabelMap[selectedInterventionType] || selectedInterventionType}。结果只用于合规危机回应对比，
            不提供个体级说服或沉默策略。
          </Paragraph>
        </div>
      </div>

      {result?.key_findings?.length ? (
        <List
          className="simulation-finding-list"
          dataSource={result.key_findings}
          header={<Text strong>关键发现</Text>}
          renderItem={(finding) => <List.Item>{finding}</List.Item>}
        />
      ) : null}
    </Card>
  )
}

function TimelinePanel({ currentStepIndex, onSelectStep, result }) {
  const steps = result?.step_results || []
  if (!steps.length) {
    return (
      <Card className="panel-card simulation-timeline-card">
        <Empty description="运行沙盘后展示步骤时间线" image={Empty.PRESENTED_IMAGE_SIMPLE} />
      </Card>
    )
  }

  return (
    <Card className="panel-card simulation-timeline-card">
      <div className="panel-heading">
        <Space>
          <GitBranch size={18} />
          <Title level={4}>模拟时间线</Title>
        </Space>
        <Tag color="cyan">{steps.length} steps</Tag>
      </div>
      <div className="simulation-timeline-list">
        {steps.map((step, index) => {
          const trend = getTrendDisplay(step.trend_direction)
          return (
            <button
              className={`simulation-timeline-item ${index === currentStepIndex ? 'active' : ''}`}
              key={step.step}
              onClick={() => onSelectStep(index)}
              type="button"
            >
              <Space direction="vertical" size={8} className="full-width">
                <Space wrap>
                  <Tag color="geekblue">Step {step.step}</Tag>
                  <Tag color={trend.color}>{trend.label}</Tag>
                  <Tag>{interventionLabelMap[step.active_intervention_type] || step.active_intervention_type}</Tag>
                </Space>
                <Text className="simulation-timeline-reason">{safeText(step.forecast_reason)}</Text>
                <div className="simulation-timeline-metrics">
                  <span>负向 {formatPercent(step.metrics.negative_ratio)}</span>
                  <span>极化 {formatNumber(step.metrics.polarization_index)}</span>
                  <span>注意力 {formatPercent(step.metrics.attention_level)}</span>
                </div>
              </Space>
            </button>
          )
        })}
      </div>
    </Card>
  )
}

function ComparisonDeltaCard({ label, value, percent = false, lowerIsBetter = true }) {
  const tone = getDeltaTone(value, lowerIsBetter)
  return (
    <div className={`simulation-delta-card simulation-delta-${tone}`}>
      <Text type="secondary">{label}</Text>
      <strong>{formatDelta(value, { percent })}</strong>
    </div>
  )
}

function VisibilityMetric({ label, value, suffix = '/100', tone = 'cyan' }) {
  return (
    <div className="simulation-visibility-metric">
      <Text type="secondary">{label}</Text>
      <strong>{Number.isFinite(Number(value)) ? Number(value).toFixed(1) : '0.0'}{suffix}</strong>
      <Tag color={tone}>{label}</Tag>
    </div>
  )
}

function VisibilityResultCard({ label, result }) {
  if (!result) {
    return (
      <div className="simulation-visibility-result-card empty">
        <Text type="secondary">{label}</Text>
        <Empty description="该方案未使用内容可见性干预" image={Empty.PRESENTED_IMAGE_SIMPLE} />
      </div>
    )
  }

  return (
    <div className="simulation-visibility-result-card">
      <Space wrap>
        <Tag color="cyan">{label}</Tag>
        <Tag color="geekblue">{interventionLabelMap[result.intervention_type] || result.intervention_type}</Tag>
        <Tag color="orange">{result.recommendation}</Tag>
      </Space>
      <div className="simulation-visibility-metric-grid">
        <VisibilityMetric label="直接曝光降低" value={result.exposure_reduction} tone="green" />
        <VisibilityMetric label="反弹风险" value={result.backlash_cost} tone="orange" />
        <VisibilityMetric label="信任损失" value={result.trust_loss} tone="red" />
        <VisibilityMetric label="跨平台外溢" value={result.spillover_risk} tone="purple" />
        <VisibilityMetric label="中立人群影响" value={result.neutral_audience_impact} tone="volcano" />
        <VisibilityMetric label="强反对群体影响" value={result.opposition_group_impact} tone="magenta" />
        <VisibilityMetric label="净风险变化" value={result.net_risk_change} tone="gold" />
        <VisibilityMetric label="删除正当性" value={result.removal_legitimacy_score} tone="blue" />
        <VisibilityMetric label="透明说明质量" value={result.public_explanation_quality_score} tone="cyan" />
      </div>
      <Paragraph className="simulation-visibility-explanation">{safeText(result.explanation)}</Paragraph>
      {result.warnings?.length ? (
        <Space wrap>
          {result.warnings.map((warning) => (
            <Tag color="orange" key={warning}>
              {warning}
            </Tag>
          ))}
        </Space>
      ) : null}
    </div>
  )
}

function VisibilityTradeoffPanel({ summary }) {
  if (!summary?.visibility_a && !summary?.visibility_b) return null

  return (
    <Card className="panel-card simulation-visibility-card">
      <div className="panel-heading">
        <Space>
          <ShieldCheck size={18} />
          <Title level={4}>内容可见性干预</Title>
        </Space>
        <Tag color="orange">人工复核建议</Tag>
      </div>
      <Alert
        className="simulation-disclaimer-alert"
        message="本模块用于评估合规内容治理动作的风险收益，不自动执行任何平台操作。"
        type="info"
        showIcon
      />
      <div className="simulation-visibility-comparison-grid">
        <VisibilityResultCard label="A 方案" result={summary.visibility_a} />
        <VisibilityResultCard label="B 方案" result={summary.visibility_b} />
      </div>
      <div className="simulation-delta-grid simulation-visibility-delta-grid">
        <ComparisonDeltaCard label="曝光降低变化" lowerIsBetter={false} value={summary.exposure_reduction_delta} />
        <ComparisonDeltaCard label="反弹风险变化" value={summary.visibility_backlash_delta} />
        <ComparisonDeltaCard label="信任损失变化" value={summary.trust_loss_delta} />
        <ComparisonDeltaCard label="跨平台外溢变化" value={summary.spillover_risk_delta} />
        <ComparisonDeltaCard label="净风险变化" value={summary.net_risk_change_delta} />
      </div>
      <div className="simulation-visibility-guidance">
        <Paragraph>
          若中立人群负面迁移明显，应优先考虑标注、澄清或透明说明，而不是直接删除。
        </Paragraph>
        <Paragraph>
          如果反弹主要集中在不可缓解的强反对群体，且内容违规清晰，删除的净风险可能较低。
        </Paragraph>
      </div>
    </Card>
  )
}

function ComparisonSummaryPanel({ summary }) {
  if (!summary) {
    return (
      <Card className="panel-card simulation-comparison-summary-card">
        <Empty description="运行 A/B 策略对比后显示聚合差异" image={Empty.PRESENTED_IMAGE_SIMPLE} />
      </Card>
    )
  }

  const betterLabel = {
    A: 'A 方案',
    B: 'B 方案',
    tie: '两方案接近',
    inconclusive: '结果不足',
  }[summary.better_option] || '结果不足'
  const summaryFields = [
    { name: 'better_option', value: summary.better_option || 'inconclusive' },
    { name: 'risk_delta', value: formatDelta(summary.risk_delta) },
    { name: 'negative_ratio_delta', value: formatDelta(summary.negative_ratio_delta, { percent: true }) },
    { name: 'polarization_delta', value: formatDelta(summary.polarization_delta) },
    { name: 'trust_recovery_delta', value: formatDelta(summary.trust_recovery_delta, { percent: true }) },
    { name: 'ethical_risk_notes', value: `${summary.ethical_risk_notes?.length || 0} notes` },
  ]

  return (
    <Card className="panel-card simulation-comparison-summary-card">
      <div className="panel-heading">
        <Space>
          <GitBranch size={18} />
          <Title level={4}>对比结果</Title>
        </Space>
        <Tag color={summary.better_option === 'B' ? 'green' : summary.better_option === 'A' ? 'blue' : 'default'}>
          {betterLabel}
        </Tag>
      </div>
      <Alert
        className="simulation-disclaimer-alert"
        message="当前为确定性沙盘模拟，不代表真实未来必然发生；推荐人工复核，不自动执行策略。"
        type="info"
        showIcon
      />
      <div className="simulation-delta-grid">
        <ComparisonDeltaCard label="风险变化" value={summary.risk_delta} />
        <ComparisonDeltaCard label="负面比例变化" value={summary.negative_ratio_delta} percent />
        <ComparisonDeltaCard label="极化变化" value={summary.polarization_delta} />
        <ComparisonDeltaCard
          label="信任恢复"
          lowerIsBetter={false}
          value={summary.trust_recovery_delta}
          percent
        />
        <ComparisonDeltaCard label="反弹风险" value={summary.backlash_risk_delta} percent />
      </div>
      <div className="simulation-summary-field-grid" aria-label="A/B comparison summary fields">
        {summaryFields.map((field) => (
          <span className="simulation-summary-field" key={field.name}>
            <span className="simulation-summary-field-name">{field.name}</span>
            <span className="simulation-summary-field-value">{field.value}</span>
          </span>
        ))}
      </div>
      <div className="simulation-review-note">
        <Text strong>人工复核建议：</Text>
        <Text> human_review_required。只用于透明危机响应方案比较，不输出个体定向建议。</Text>
      </div>
      <div className="simulation-ethics-notes">
        {(summary.ethical_risk_notes || []).map((note) => (
          <Tag color="geekblue" key={note}>
            {note}
          </Tag>
        ))}
      </div>
    </Card>
  )
}

function ComparisonScenarioPanel({
  label,
  interventionType,
  metrics,
  onInterventionChange,
  options,
  result,
  scenario,
  stepIndex,
  stepResult,
}) {
  return (
    <div className="simulation-comparison-panel">
      <div className="simulation-comparison-header">
        <Space direction="vertical" size={4}>
          <Title level={4}>{label}</Title>
          <Text type="secondary">{interventionLabelMap[interventionType] || interventionType}</Text>
        </Space>
        <Select
          className="simulation-comparison-select"
          onChange={onInterventionChange}
          options={options}
          value={interventionType}
        />
      </div>
      <BubbleCanvas
        compact
        currentStepIndex={stepIndex}
        initialMetrics={result?.initial_metrics || deriveInitialMetrics(scenario?.agents || [])}
        metrics={metrics}
        scenario={scenario}
        stepResult={stepResult}
        title={`${label} 泡泡视图`}
      />
      <div className="simulation-comparison-metrics">
        <span>负面 {formatPercent(metrics?.negative_ratio)}</span>
        <span>极化 {formatNumber(metrics?.polarization_index)}</span>
        <span>注意力 {formatPercent(metrics?.attention_level)}</span>
        <span>信任 {formatPercent(metrics?.trust_recovery_proxy)}</span>
      </div>
    </div>
  )
}

function ComparisonTimelinePanel({ currentStepIndex, onSelectStep, resultA, resultB }) {
  const stepsA = resultA?.step_results || []
  const stepsB = resultB?.step_results || []
  const maxSteps = Math.max(stepsA.length, stepsB.length)

  if (!maxSteps) {
    return (
      <Card className="panel-card simulation-timeline-card">
        <Empty description="运行 A/B 对比后显示 A timeline / B timeline" image={Empty.PRESENTED_IMAGE_SIMPLE} />
      </Card>
    )
  }

  return (
    <Card className="panel-card simulation-timeline-card">
      <div className="panel-heading">
        <Space>
          <GitBranch size={18} />
          <Title level={4}>A/B 时间线对比</Title>
        </Space>
        <Tag color="cyan">final step comparison</Tag>
      </div>
      <div className="simulation-comparison-timeline">
        {Array.from({ length: maxSteps }).map((_, index) => {
          const stepA = stepsA[index]
          const stepB = stepsB[index]
          const delta = (stepB?.metrics?.negative_ratio ?? 0) - (stepA?.metrics?.negative_ratio ?? 0)
          return (
            <button
              className={`simulation-timeline-item ${index === currentStepIndex ? 'active' : ''}`}
              key={`compare-step-${index + 1}`}
              onClick={() => onSelectStep(index)}
              type="button"
            >
              <Space direction="vertical" size={8} className="full-width">
                <Space wrap>
                  <Tag color="geekblue">Step {index + 1}</Tag>
                  <Tag color={getDeltaTone(delta)}>B-A 负面 {formatDelta(delta, { percent: true })}</Tag>
                </Space>
                <div className="simulation-timeline-metrics">
                  <span>A 负面 {formatPercent(stepA?.metrics?.negative_ratio)}</span>
                  <span>B 负面 {formatPercent(stepB?.metrics?.negative_ratio)}</span>
                  <span>A 极化 {formatNumber(stepA?.metrics?.polarization_index)}</span>
                  <span>B 极化 {formatNumber(stepB?.metrics?.polarization_index)}</span>
                  <span>A 注意力 {formatPercent(stepA?.metrics?.attention_level)}</span>
                  <span>B 注意力 {formatPercent(stepB?.metrics?.attention_level)}</span>
                </div>
              </Space>
            </button>
          )
        })}
      </div>
    </Card>
  )
}

function SafetyNotice({ policy }) {
  return (
    <Card className="panel-card simulation-safety-card">
      <div className="panel-heading">
        <Space>
          <ShieldCheck size={18} />
          <Title level={4}>伦理边界</Title>
        </Space>
        <Space wrap>
          <Tag color="cyan">离线确定性</Tag>
          <Tag color="cyan">确定性 MVP</Tag>
          <Tag color="green">聚合级输出</Tag>
        </Space>
      </div>
      <Space wrap>
        <Tag color="geekblue">不调用真实 API</Tag>
        <Tag color="geekblue">不调用真实 LLM</Tag>
        <Tag color="green">不提供个体定向</Tag>
        <Tag color="green">不暴露禁用干预</Tag>
        <Tag color="default">不代表真实未来必然发生</Tag>
      </Space>
      <Paragraph className="simulation-policy-copy">
        {safeText(policy?.policy_summary, '仅支持透明、合规、聚合级危机回应方案比较。')}
      </Paragraph>
    </Card>
  )
}

function CaseInitializationPanel({
  caseOptions,
  initializationLoading,
  initializationResult,
  onCaseIdChange,
  onInitialize,
  onPreview,
  selectedCaseId,
}) {
  return (
    <Card className="panel-card simulation-initializer-card">
      <div className="panel-heading">
        <Space>
          <GitBranch size={18} />
          <Title level={4}>从案例初始化沙盘</Title>
        </Space>
        <Tag color="cyan">aggregate</Tag>
      </div>

      <Space direction="vertical" size={12} className="full-width">
        <Alert
          message="仅基于聚合数据，不生成个体操控建议"
          description="初始化会读取案例分析、话题风险、监控快照、预警和预测摘要；不会调用真实 API 或 LLM。"
          type="info"
          showIcon
        />

        <div>
          <Text type="secondary">选择案例</Text>
          <Select
            allowClear
            className="full-width"
            notFoundContent="暂无案例列表，可在下方输入 case_id"
            onChange={(value) => onCaseIdChange(value || '')}
            options={caseOptions}
            placeholder="选择已完成分析的案例"
            showSearch
            value={selectedCaseId || undefined}
          />
        </div>

        <div>
          <Text type="secondary">case_id</Text>
          <Input
            onChange={(event) => onCaseIdChange(event.target.value)}
            placeholder="例如 case_001"
            value={selectedCaseId}
          />
        </div>

        <Space wrap>
          <Button loading={initializationLoading} onClick={onPreview}>
            预览初始化
          </Button>
          <Button loading={initializationLoading} onClick={onInitialize} type="primary">
            从案例初始化沙盘
          </Button>
        </Space>

        <InitializationSummaryCard result={initializationResult} />
      </Space>
    </Card>
  )
}

function InitializationSummaryCard({ result }) {
  if (!result) {
    return (
      <div className="simulation-initializer-empty">
        <Text type="secondary">可先预览事件框体、人群分布与回音壁偏差，再加载为沙盘场景。</Text>
      </div>
    )
  }
  const eventFrame = result.event_frame || {}
  const subIssues = eventFrame.sub_issues || []
  const segments = result.audience_segments || []
  const baseline = eventFrame.baseline_public_profile || {}
  const gap = result.frame_gap_analysis || eventFrame.frame_gap_analysis || {}
  const implications = result.strategy_implications || []
  const warnings = result.warnings || []

  return (
    <div className="simulation-initializer-summary">
      <div className="simulation-initializer-section">
        <Text type="secondary">事件框体</Text>
        <Title level={5}>{safeText(eventFrame.event_title, '未命名事件')}</Title>
        <Paragraph>{safeText(eventFrame.event_summary, '暂无摘要')}</Paragraph>
      </div>

      <div className="simulation-initializer-section">
        <Text type="secondary">子议题</Text>
        <Space wrap>
          {subIssues.slice(0, 4).map((issue) => {
            const issueRiskScore = issue.risk_score ?? issue.topic_risk_score ?? 0
            return (
              <Tag color={issueRiskScore >= 70 ? 'red' : issueRiskScore >= 40 ? 'orange' : 'cyan'} key={issue.sub_issue_id}>
                {issue.title} {Math.round(issueRiskScore)}
              </Tag>
            )
          })}
          {!subIssues.length ? <Tag>暂无子议题</Tag> : null}
        </Space>
      </div>

      <div className="simulation-initializer-section">
        <Text type="secondary">人群分布</Text>
        <div className="simulation-audience-list">
          {segments.slice(0, 6).map((segment) => (
            <div className="simulation-audience-row" key={segment.segment_id}>
              <span>{segment.label || segment.segment_id}</span>
              <Tag color={segment.color_hint || 'default'}>{formatPercent(segment.proportion)}</Tag>
            </div>
          ))}
        </div>
      </div>

      <div className="simulation-initializer-section">
        <Text type="secondary">普通公众基线</Text>
        <Space wrap>
          <Tag color="geekblue">{safeText(baseline.event_category, 'unknown')}</Tag>
          <Tag>expected {formatNumber(baseline.expected_average_reaction ?? 0)}</Tag>
        </Space>
      </div>

      <div className="simulation-initializer-section">
        <Text type="secondary">回音壁偏差</Text>
        <Space wrap>
          <Tag color={gap.primary_classification === 'insufficient_data' ? 'orange' : 'cyan'}>
            {safeText(gap.primary_classification, 'unknown')}
          </Tag>
          {(gap.secondary_classifications || []).map((item) => (
            <Tag color="purple" key={item}>
              {item}
            </Tag>
          ))}
        </Space>
        <Paragraph>{safeText(gap.summary, '暂无偏差说明')}</Paragraph>
      </div>

      <div className="simulation-initializer-section">
        <Text type="secondary">策略提示</Text>
        {implications.slice(0, 2).map((item) => (
          <Paragraph key={item.implication_id}>{safeText(item.rationale)}</Paragraph>
        ))}
      </div>

      {warnings.length ? (
        <Alert
          message="数据不足 / 初始化警告"
          description={warnings.join('；')}
          type="warning"
          showIcon
        />
      ) : null}
    </div>
  )
}

function buildStrategyReportPayload({
  comparisonResult,
  interventionA,
  interventionB,
  runResult,
  scenario,
  selectedIntervention,
  viewMode,
}) {
  if (viewMode === 'comparison') {
    if (!comparisonResult?.resultA || !comparisonResult?.resultB) return null
    return {
      simulation_mode: 'comparison',
      scenario_name: scenario?.name || comparisonResult.resultA.scenario_name || 'Simulation scenario',
      intervention_a: interventionA,
      intervention_b: interventionB,
      result_a: comparisonResult.resultA,
      result_b: comparisonResult.resultB,
      comparison_summary: comparisonResult.comparisonSummary || null,
      generated_from: 'simulation_lab_ui',
    }
  }
  if (!runResult) return null
  return {
    simulation_mode: 'single',
    scenario_name: scenario?.name || runResult.scenario_name || 'Simulation scenario',
    intervention_a: selectedIntervention,
    run_result: runResult,
    generated_from: 'simulation_lab_ui',
  }
}

function StrategyReportExportCard({
  canExport,
  loading,
  mode,
  onCopy,
  onDownload,
  onExport,
  report,
  status,
}) {
  const markdown = report?.markdown || ''
  return (
    <Card className="panel-card simulation-report-card">
      <div className="panel-heading">
        <Space>
          <FileText size={18} />
          <Title level={4}>策略预演报告</Title>
        </Space>
        <Tag color="cyan">Markdown</Tag>
      </div>
      <Alert
        className="simulation-disclaimer-alert"
        message="当前结果不代表真实未来必然发生；报告仅用于聚合级方案复核，不会自动执行任何现实处置。"
        type="info"
        showIcon
      />
      <Space direction="vertical" size={12} className="full-width">
        <Space wrap>
          <Button disabled={!canExport} icon={<FileText size={16} />} loading={loading} onClick={onExport} type="primary">
            导出策略预演报告
          </Button>
          <Button disabled={!markdown} icon={<Copy size={16} />} onClick={onCopy}>
            复制 Markdown
          </Button>
          <Button disabled={!markdown} icon={<Download size={16} />} onClick={onDownload}>
            下载 .md
          </Button>
        </Space>
        <Space wrap>
          <Tag color={mode === 'comparison' ? 'geekblue' : 'green'}>
            {mode === 'comparison' ? 'A/B 策略对比' : '单场景模拟'}
          </Tag>
          <Tag color="orange">人工复核问题</Tag>
          <Tag color="volcano">伦理风险提示</Tag>
          <Tag>模拟限制说明</Tag>
        </Space>
        {status ? <Text type="secondary">{status}</Text> : null}
        {markdown ? (
          <div className="simulation-report-preview-shell">
            <Text strong>Markdown preview</Text>
            <pre className="simulation-report-preview">{markdown.slice(0, 900)}</pre>
          </div>
        ) : (
          <Text type="secondary">运行模拟或 A/B 对比后，可导出安全 Markdown 报告。</Text>
        )}
      </Space>
    </Card>
  )
}

export function SimulationLab({ cases = [], currentCase = null } = {}) {
  const [scenario, setScenario] = useState(null)
  const [originalScenario, setOriginalScenario] = useState(null)
  const [ethicsPolicy, setEthicsPolicy] = useState(null)
  const [initializationResult, setInitializationResult] = useState(null)
  const [selectedCaseId, setSelectedCaseId] = useState(currentCase?.case_id || '')
  const [viewMode, setViewMode] = useState('single')
  const [selectedIntervention, setSelectedIntervention] = useState('clarification')
  const [interventionA, setInterventionA] = useState('no_response')
  const [interventionB, setInterventionB] = useState('clarification')
  const [steps, setSteps] = useState(6)
  const [runResult, setRunResult] = useState(null)
  const [comparisonResult, setComparisonResult] = useState(null)
  const [currentStepIndex, setCurrentStepIndex] = useState(-1)
  const [comparisonStepIndex, setComparisonStepIndex] = useState(-1)
  const [loading, setLoading] = useState(false)
  const [running, setRunning] = useState(false)
  const [comparisonRunning, setComparisonRunning] = useState(false)
  const [initializationLoading, setInitializationLoading] = useState(false)
  const [strategyReport, setStrategyReport] = useState(null)
  const [strategyReportLoading, setStrategyReportLoading] = useState(false)
  const [strategyReportStatus, setStrategyReportStatus] = useState('')
  const [error, setError] = useState('')

  const caseOptions = useMemo(
    () =>
      (cases || []).map((item) => ({
        label: item.title ? `${item.title} (${item.case_id})` : item.case_id,
        value: item.case_id,
      })),
    [cases],
  )
  const allowedOptions = useMemo(() => getAllowedOptions(ethicsPolicy), [ethicsPolicy])
  const activeStep = currentStepIndex >= 0 ? runResult?.step_results?.[currentStepIndex] : null
  const initialMetrics = runResult?.initial_metrics || deriveInitialMetrics(scenario?.agents || [])
  const currentMetrics = activeStep?.metrics || runResult?.final_metrics || initialMetrics
  const eventCards = useMemo(
    () => getEventCards(scenario, selectedIntervention),
    [scenario, selectedIntervention],
  )
  const comparisonBaseScenario = originalScenario || scenario
  const comparisonScenarioA = comparisonBaseScenario
    ? buildScenarioForRun(comparisonBaseScenario, interventionA, steps)
    : null
  const comparisonScenarioB = comparisonBaseScenario
    ? buildScenarioForRun(comparisonBaseScenario, interventionB, steps)
    : null
  const comparisonStepA =
    comparisonStepIndex >= 0 ? comparisonResult?.resultA?.step_results?.[comparisonStepIndex] : null
  const comparisonStepB =
    comparisonStepIndex >= 0 ? comparisonResult?.resultB?.step_results?.[comparisonStepIndex] : null
  const comparisonMetricsA =
    comparisonStepA?.metrics ||
    getFinalMetrics(comparisonResult?.resultA) ||
    deriveInitialMetrics(comparisonBaseScenario?.agents || [])
  const comparisonMetricsB =
    comparisonStepB?.metrics ||
    getFinalMetrics(comparisonResult?.resultB) ||
    deriveInitialMetrics(comparisonBaseScenario?.agents || [])
  const canExportStrategyReport = viewMode === 'comparison' ? Boolean(comparisonResult) : Boolean(runResult)

  const loadDemoScenario = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const [policy, demoScenario] = await Promise.all([
        getSimulationEthicsPolicy().catch(() => null),
        getSimulationDemoScenario(),
      ])
      setEthicsPolicy(policy)
      setScenario(demoScenario)
      setOriginalScenario(demoScenario)
      setInitializationResult(null)
      const firstAllowed = demoScenario.interventions?.[0]?.intervention_type || 'clarification'
      const options = getAllowedOptions(policy)
      const optionValues = options.map((option) => option.value)
      setSelectedIntervention(optionValues.includes(firstAllowed) ? firstAllowed : optionValues[0] || 'clarification')
      setInterventionA(optionValues.includes('no_response') ? 'no_response' : optionValues[0] || 'clarification')
      setInterventionB(
        optionValues.includes('content_removal_with_explanation')
          ? 'content_removal_with_explanation'
          : optionValues.includes('clarification')
            ? 'clarification'
            : optionValues[1] || optionValues[0] || 'clarification',
      )
      setSteps(demoScenario.config?.steps || 6)
      setRunResult(null)
      setComparisonResult(null)
      setStrategyReport(null)
      setStrategyReportStatus('')
      setCurrentStepIndex(-1)
      setComparisonStepIndex(-1)
    } catch (requestError) {
      setError(getErrorMessage(requestError, '无法加载 Simulation Lab 演示场景。'))
      setScenario(null)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadDemoScenario()
  }, [loadDemoScenario])

  useEffect(() => {
    if (currentCase?.case_id && !selectedCaseId) {
      setSelectedCaseId(currentCase.case_id)
    }
  }, [currentCase, selectedCaseId])

  const applyInitializationResult = useCallback(
    (result) => {
      setInitializationResult(result)
      const initializedScenario = result?.simulation_scenario
      if (initializedScenario?.scenario_id) {
        setScenario(initializedScenario)
        setOriginalScenario(initializedScenario)
        setViewMode('single')
        const preferred =
          initializedScenario.interventions?.[0]?.intervention_type ||
          result?.event_frame?.initialization_hints?.recommended_default_intervention ||
          'clarification'
        const optionValues = allowedOptions.map((option) => option.value)
        setSelectedIntervention(optionValues.includes(preferred) ? preferred : optionValues[0] || 'clarification')
        setInterventionA(optionValues.includes('no_response') ? 'no_response' : optionValues[0] || 'clarification')
        setInterventionB(optionValues.includes(preferred) ? preferred : optionValues[1] || optionValues[0] || 'clarification')
        setSteps(initializedScenario.config?.steps || 6)
        setRunResult(null)
        setComparisonResult(null)
        setStrategyReport(null)
        setStrategyReportStatus('')
        setCurrentStepIndex(-1)
        setComparisonStepIndex(-1)
      }
    },
    [allowedOptions],
  )

  const handlePreviewCaseInitialization = useCallback(async () => {
    if (!selectedCaseId) {
      setError('请输入或选择 case_id 后再预览初始化。')
      return
    }
    setInitializationLoading(true)
    setError('')
    try {
      const result = await previewCaseSimulationInitialization(selectedCaseId)
      setInitializationResult(result)
    } catch (requestError) {
      setError(getErrorMessage(requestError, '无法预览案例初始化结果。'))
    } finally {
      setInitializationLoading(false)
    }
  }, [selectedCaseId])

  const handleInitializeFromCase = useCallback(async () => {
    if (!selectedCaseId) {
      setError('请输入或选择 case_id 后再初始化沙盘。')
      return
    }
    setInitializationLoading(true)
    setError('')
    try {
      const result = await initializeCaseSimulation(selectedCaseId)
      applyInitializationResult(result)
    } catch (requestError) {
      setError(getErrorMessage(requestError, '无法从案例初始化 Simulation Lab。'))
    } finally {
      setInitializationLoading(false)
    }
  }, [applyInitializationResult, selectedCaseId])

  const handleRunSimulation = useCallback(async () => {
    if (!scenario) {
      setError('请先加载演示场景。')
      return
    }
    if (FORBIDDEN_INTERVENTIONS.has(selectedIntervention)) {
      setError('该干预类型被伦理策略禁止。')
      return
    }
    setRunning(true)
    setError('')
    try {
      const nextScenario = buildScenarioForRun(scenario, selectedIntervention, steps)
      const response = await runSimulation(nextScenario)
      setScenario(nextScenario)
      setRunResult(response)
      setStrategyReport(null)
      setStrategyReportStatus('')
      setCurrentStepIndex(response.step_results.length ? 0 : -1)
    } catch (requestError) {
      setError(getErrorMessage(requestError, '无法运行确定性沙盘模拟。'))
    } finally {
      setRunning(false)
    }
  }, [scenario, selectedIntervention, steps])

  const handleRunComparison = useCallback(async () => {
    const baseScenario = originalScenario || scenario
    if (!baseScenario) {
      setError('请先加载演示场景。')
      return
    }
    if (FORBIDDEN_INTERVENTIONS.has(interventionA) || FORBIDDEN_INTERVENTIONS.has(interventionB)) {
      setError('A/B 对比中包含被伦理策略禁止的干预类型。')
      return
    }

    setComparisonRunning(true)
    setError('')
    try {
      const scenarioA = buildScenarioForRun(baseScenario, interventionA, steps)
      const scenarioB = buildScenarioForRun(baseScenario, interventionB, steps)
      const [resultA, resultB] = await Promise.all([runSimulation(scenarioA), runSimulation(scenarioB)])
      setComparisonResult({
        resultA,
        resultB,
        comparisonSummary: buildComparisonSummary(resultA, resultB, interventionA, interventionB),
      })
      setStrategyReport(null)
      setStrategyReportStatus('')
      setComparisonStepIndex(resultA.step_results.length || resultB.step_results.length ? 0 : -1)
    } catch (requestError) {
      setError(getErrorMessage(requestError, '无法运行 A/B 策略对比。'))
    } finally {
      setComparisonRunning(false)
    }
  }, [interventionA, interventionB, originalScenario, scenario, steps])

  const handleStepForward = useCallback(async () => {
    if (!runResult) {
      await handleRunSimulation()
      return
    }
    const nextIndex = Math.min(currentStepIndex + 1, runResult.step_results.length - 1)
    setCurrentStepIndex(nextIndex)
  }, [currentStepIndex, handleRunSimulation, runResult])

  const handleComparisonStepForward = useCallback(async () => {
    if (!comparisonResult) {
      await handleRunComparison()
      return
    }
    const maxIndex = Math.max(
      comparisonResult.resultA?.step_results?.length || 0,
      comparisonResult.resultB?.step_results?.length || 0,
    ) - 1
    setComparisonStepIndex(Math.min(comparisonStepIndex + 1, Math.max(maxIndex, 0)))
  }, [comparisonResult, comparisonStepIndex, handleRunComparison])

  const handleReset = useCallback(() => {
    setScenario(originalScenario)
    setInitializationResult(null)
    setRunResult(null)
    setComparisonResult(null)
    setStrategyReport(null)
    setStrategyReportStatus('')
    setCurrentStepIndex(-1)
    setComparisonStepIndex(-1)
    setError('')
    if (originalScenario?.config?.steps) {
      setSteps(originalScenario.config.steps)
    }
  }, [originalScenario])

  const handleExportStrategyReport = useCallback(async () => {
    const payload = buildStrategyReportPayload({
      comparisonResult,
      interventionA,
      interventionB,
      runResult,
      scenario,
      selectedIntervention,
      viewMode,
    })
    if (!payload) {
      setStrategyReportStatus('请先运行模拟或 A/B 对比，再导出策略预演报告。')
      return
    }
    setStrategyReportLoading(true)
    setStrategyReportStatus('')
    setError('')
    try {
      const response = await exportSimulationStrategyMarkdownReport(payload)
      setStrategyReport(response)
      setStrategyReportStatus('策略预演报告已生成，可复制 Markdown 或下载 .md。')
    } catch (requestError) {
      setStrategyReport(null)
      setStrategyReportStatus(getErrorMessage(requestError, '无法导出策略预演报告。'))
    } finally {
      setStrategyReportLoading(false)
    }
  }, [comparisonResult, interventionA, interventionB, runResult, scenario, selectedIntervention, viewMode])

  const handleCopyStrategyReport = useCallback(async () => {
    if (!strategyReport?.markdown) return
    if (!navigator.clipboard?.writeText) {
      setStrategyReportStatus('当前浏览器不支持直接复制，请使用下载 .md。')
      return
    }
    await navigator.clipboard.writeText(strategyReport.markdown)
    setStrategyReportStatus('Markdown 已复制。')
  }, [strategyReport])

  const handleDownloadStrategyReport = useCallback(() => {
    if (!strategyReport?.markdown) return
    const blob = new Blob([strategyReport.markdown], { type: 'text/markdown;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = 'simulation-strategy-report.md'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
    setStrategyReportStatus('Markdown 文件已准备下载。')
  }, [strategyReport])

  return (
    <div className="page-stack simulation-lab-page">
      <div className="page-heading">
        <div>
          <Title level={2}>舆情预演沙盘</Title>
          <Paragraph>
            用合成代理泡泡、社群区域和聚合指标展示伦理危机回应方案的确定性模拟；页面不会触发真实 API、
            不调用真实大模型，也不输出个体级定向建议。
          </Paragraph>
        </div>
        <Space wrap>
          <Tag color="cyan" className="large-tag">
            Simulation Lab
          </Tag>
          <Tag color="green" className="large-tag">
            Aggregate Only
          </Tag>
        </Space>
      </div>

      {error ? <Alert message="Simulation Lab 加载失败" description={error} type="error" showIcon /> : null}

      <Skeleton active loading={loading} paragraph={{ rows: 8 }}>
        <Card className="panel-card simulation-mode-card">
          <div className="simulation-mode-toolbar">
            <Space direction="vertical" size={4}>
              <Title level={4}>模拟模式</Title>
              <Text type="secondary">单场景解释或 A/B 策略对比都基于同一份离线合成场景。</Text>
            </Space>
            <Segmented
              onChange={(value) => {
                setViewMode(value)
                setStrategyReport(null)
                setStrategyReportStatus('')
              }}
              options={[
                { label: '单场景模拟', value: 'single' },
                { label: 'A/B 策略对比', value: 'comparison' },
              ]}
              value={viewMode}
            />
          </div>
          {viewMode === 'comparison' ? (
            <Alert
              className="simulation-disclaimer-alert"
              message="本模块只用于透明危机响应方案比较；不提供个体定向操控建议，不支持虚假共识、机器人放大、伪造事件或隐蔽操纵。"
              type="info"
              showIcon
            />
          ) : null}
        </Card>

        <Row gutter={[16, 16]} align="stretch">
          <Col span={viewMode === 'comparison' ? 7 : 6}>
            <Space direction="vertical" size={16} className="full-width">
              <Card className="panel-card simulation-control-card">
                <div className="panel-heading">
                  <Space>
                    <RadioTower size={18} />
                    <Title level={4}>场景控制</Title>
                  </Space>
                  <Tag color="cyan">MVP</Tag>
                </div>

                {scenario ? (
                  <Space direction="vertical" size={14} className="full-width">
                    <div>
                      <Text type="secondary">当前场景</Text>
                      <Title level={5}>{safeText(scenario.name, 'Demo Scenario')}</Title>
                      <Paragraph className="simulation-scenario-copy">{safeText(scenario.description)}</Paragraph>
                    </div>

                    {viewMode === 'single' ? (
                      <div>
                        <Text type="secondary">干预类型</Text>
                        <Select
                          className="full-width"
                          onChange={(value) => {
                            setSelectedIntervention(value)
                            setRunResult(null)
                            setCurrentStepIndex(-1)
                            setStrategyReport(null)
                            setStrategyReportStatus('')
                          }}
                          options={allowedOptions}
                          value={selectedIntervention}
                        />
                      </div>
                    ) : (
                      <Space direction="vertical" size={12} className="full-width">
                        <div>
                          <Text type="secondary">A 方案</Text>
                          <Select
                            className="full-width"
                            onChange={(value) => {
                              setInterventionA(value)
                              setComparisonResult(null)
                              setComparisonStepIndex(-1)
                              setStrategyReport(null)
                              setStrategyReportStatus('')
                            }}
                            options={allowedOptions}
                            value={interventionA}
                          />
                        </div>
                        <div>
                          <Text type="secondary">B 方案</Text>
                          <Select
                            className="full-width"
                            onChange={(value) => {
                              setInterventionB(value)
                              setComparisonResult(null)
                              setComparisonStepIndex(-1)
                              setStrategyReport(null)
                              setStrategyReportStatus('')
                            }}
                            options={allowedOptions}
                            value={interventionB}
                          />
                        </div>
                      </Space>
                    )}

                    <div>
                      <Text type="secondary">模拟步数</Text>
                      <InputNumber
                        className="full-width"
                        min={1}
                        max={24}
                        onChange={(value) => {
                          setSteps(Number(value || 1))
                          setRunResult(null)
                          setComparisonResult(null)
                          setCurrentStepIndex(-1)
                          setComparisonStepIndex(-1)
                          setStrategyReport(null)
                          setStrategyReportStatus('')
                        }}
                        value={steps}
                      />
                    </div>

                    <Space wrap>
                      <Button icon={<RefreshCw size={16} />} onClick={loadDemoScenario}>
                        加载演示场景
                      </Button>
                      <Button icon={<RotateCcw size={16} />} onClick={handleReset}>
                        重置
                      </Button>
                    </Space>

                    {viewMode === 'single' ? (
                      <Space wrap>
                        <Button
                          icon={<PlayCircle size={16} />}
                          loading={running}
                          onClick={handleRunSimulation}
                          type="primary"
                        >
                          运行模拟
                        </Button>
                        <Button icon={<StepForward size={16} />} onClick={handleStepForward}>
                          单步推进
                        </Button>
                      </Space>
                    ) : (
                      <Space wrap>
                        <Button
                          icon={<PlayCircle size={16} />}
                          loading={comparisonRunning}
                          onClick={handleRunComparison}
                          type="primary"
                        >
                          运行 A/B 对比
                        </Button>
                        <Button icon={<StepForward size={16} />} onClick={handleComparisonStepForward}>
                          单步对比
                        </Button>
                      </Space>
                    )}
                  </Space>
                ) : (
                  <Empty description="未加载场景" image={Empty.PRESENTED_IMAGE_SIMPLE}>
                    <Button onClick={loadDemoScenario} type="primary">
                      加载演示场景
                    </Button>
                  </Empty>
                )}
              </Card>

              <CaseInitializationPanel
                caseOptions={caseOptions}
                initializationLoading={initializationLoading}
                initializationResult={initializationResult}
                onCaseIdChange={(value) => setSelectedCaseId(value)}
                onInitialize={handleInitializeFromCase}
                onPreview={handlePreviewCaseInitialization}
                selectedCaseId={selectedCaseId}
              />

              <SafetyNotice policy={ethicsPolicy} />

              <StrategyReportExportCard
                canExport={canExportStrategyReport}
                loading={strategyReportLoading}
                mode={viewMode}
                onCopy={handleCopyStrategyReport}
                onDownload={handleDownloadStrategyReport}
                onExport={handleExportStrategyReport}
                report={strategyReport}
                status={strategyReportStatus}
              />

              {viewMode === 'comparison' ? (
                <Card className="panel-card simulation-ab-card">
                  <Title level={4}>人工复核建议</Title>
                  <Paragraph>
                    A/B 结果只比较聚合指标，不会自动执行策略；真实处置需要结合事实、平台规则和人工审核。
                  </Paragraph>
                </Card>
              ) : null}
            </Space>
          </Col>

          {viewMode === 'single' ? (
            <>
              <Col span={12}>
                <Space direction="vertical" size={16} className="full-width">
                  <Card className="panel-card simulation-event-panel">
                    <div className="panel-heading">
                      <Space>
                        <Waves size={18} />
                        <Title level={4}>消息 / 干预事件</Title>
                      </Space>
                      <Tag color="orange">step-based pulse</Tag>
                    </div>
                    <EventCards events={eventCards} activeInterventionType={activeStep?.active_intervention_type} />
                  </Card>
                  <BubbleCanvas
                    currentStepIndex={currentStepIndex}
                    initialMetrics={initialMetrics}
                    metrics={currentMetrics}
                    scenario={scenario}
                    stepResult={activeStep}
                  />
                </Space>
              </Col>

              <Col span={6}>
                <Space direction="vertical" size={16} className="full-width">
                  <MetricsPanel metrics={currentMetrics} result={runResult} />
                  <ExplanationPanel
                    metrics={currentMetrics}
                    result={runResult}
                    selectedInterventionType={selectedIntervention}
                    stepResult={activeStep}
                  />
                </Space>
              </Col>
            </>
          ) : (
            <Col span={17}>
              <Space direction="vertical" size={16} className="full-width">
                <ComparisonSummaryPanel summary={comparisonResult?.comparisonSummary} />
                <VisibilityTradeoffPanel summary={comparisonResult?.comparisonSummary} />
                <div className="simulation-comparison-grid">
                  <ComparisonScenarioPanel
                    interventionType={interventionA}
                    label="A 方案"
                    metrics={comparisonMetricsA}
                    onInterventionChange={(value) => {
                      setInterventionA(value)
                      setComparisonResult(null)
                      setComparisonStepIndex(-1)
                      setStrategyReport(null)
                      setStrategyReportStatus('')
                    }}
                    options={allowedOptions}
                    result={comparisonResult?.resultA}
                    scenario={comparisonScenarioA}
                    stepIndex={comparisonStepIndex}
                    stepResult={comparisonStepA}
                  />
                  <ComparisonScenarioPanel
                    interventionType={interventionB}
                    label="B 方案"
                    metrics={comparisonMetricsB}
                    onInterventionChange={(value) => {
                      setInterventionB(value)
                      setComparisonResult(null)
                      setComparisonStepIndex(-1)
                      setStrategyReport(null)
                      setStrategyReportStatus('')
                    }}
                    options={allowedOptions}
                    result={comparisonResult?.resultB}
                    scenario={comparisonScenarioB}
                    stepIndex={comparisonStepIndex}
                    stepResult={comparisonStepB}
                  />
                </div>
              </Space>
            </Col>
          )}
        </Row>

        {viewMode === 'single' ? (
          <TimelinePanel currentStepIndex={currentStepIndex} onSelectStep={setCurrentStepIndex} result={runResult} />
        ) : (
          <ComparisonTimelinePanel
            currentStepIndex={comparisonStepIndex}
            onSelectStep={setComparisonStepIndex}
            resultA={comparisonResult?.resultA}
            resultB={comparisonResult?.resultB}
          />
        )}
      </Skeleton>
    </div>
  )
}
