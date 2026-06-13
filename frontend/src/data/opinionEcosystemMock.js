export const BOX_WIDTH = 760
export const BOX_HEIGHT = 520
export const PEOPLE_CLUSTER_COUNT = 164

export const OPINION_STATE_COLORS = {
  support: '#54f5a8',
  neutral: '#a7b0c4',
  oppose: '#ff5d8f',
  uncertain: '#f5c44b',
  bridge: '#a478ff',
  withdrawn: '#667085',
}

export const OPINION_STATE_LABELS = {
  support: '支持簇',
  neutral: '中立参与',
  oppose: '反对簇',
  uncertain: '摇摆观望',
  bridge: '桥接人群簇',
  withdrawn: '退出讨论',
}

export const OPINION_ECOSYSTEM_SCHEMA_STATUS = [
  ['EchoBox', '回音壁容器'],
  ['PeopleCluster', '人群簇，不是个人'],
  ['InfluenceCore', '观念 / 内容 / 媒体 / 官方 / 梗化核心，不是小球'],
  ['CampDynamics', '同化 / 中立化 / 退出 / 反噬 / 再激活的 mock 规则'],
  ['ResponseTempo', '处理节奏建议'],
  ['Current status', '当前仍为静态 mock 数据'],
]

export const HOW_TO_READ = [
  ['EchoBox', '回音壁容器，边框厚度与光晕代表讨论边界强度。'],
  ['Small balls', '人群簇，不代表真实个体、账号画像或个人身份。'],
  ['Influence cores', '观念、内容、媒体、官方说明或梗化核心，不是人群球。'],
  ['Color change', '公开表达状态迁移：同化、中立化、退出、反噬或解构。'],
  ['Fade out', '退出当前事件讨论，不代表问题已经解决。'],
]

const PARAMETER_SOURCE = 'frontend_mock_schema_v1'

const CAMP_STATE_VISUALS = {
  support_core: { key: 'support', label: '正方核心', color: OPINION_STATE_COLORS.support },
  support_soft: { key: 'support', label: '温和支持', color: OPINION_STATE_COLORS.support },
  neutral_observing: { key: 'uncertain', label: '中立围观', color: OPINION_STATE_COLORS.uncertain },
  neutral_engaged: { key: 'neutral', label: '中立参与', color: OPINION_STATE_COLORS.neutral },
  oppose_soft: { key: 'oppose', label: '温和反对', color: OPINION_STATE_COLORS.oppose },
  oppose_core: { key: 'oppose', label: '反方核心', color: OPINION_STATE_COLORS.oppose },
  oppose_extreme: { key: 'oppose', label: '高强度反对', color: OPINION_STATE_COLORS.oppose },
  withdrawn: { key: 'withdrawn', label: '退出讨论', color: OPINION_STATE_COLORS.withdrawn },
  dormant_grievance: { key: 'uncertain', label: '潜伏不满', color: OPINION_STATE_COLORS.uncertain },
}

const BASE_ECHO_BOX = {
  box_id: 'mock_echo_box_001',
  case_id: 'frontend_mock_case',
  label: '静态舆论回音壁',
  platform: 'frontend_mock',
  box_type: 'event_discussion_container',
  echo_chamber_score: 0.58,
  carrying_capacity: 1,
  saturation_ratio: 0.62,
  permeability_score: 0.38,
  internal_reinforcement: 0.57,
  external_inflow_rate: 0.28,
  fatigue_rate: 0.22,
  breakout_risk: 0.32,
  lifecycle_stage: 'active_observation',
  confidence: 0.72,
  parameter_source: PARAMETER_SOURCE,
}

const BASE_INFLUENCE_CORES = [
  {
    core_id: 'opposition',
    core_type: 'content_core',
    label: '反方核心视频',
    stance_label: '质疑叙事',
    stance_score: -0.72,
    source_type: 'video',
    source_credibility: 0.48,
    evidence_strength: 0.42,
    logic_strength: 0.46,
    emotional_intensity: 0.78,
    extremity_score: 0.68,
    gravitational_pull: 0.42,
    neutral_acceptance: 0.2,
    same_camp_reinforcement: 0.72,
    opponent_resistance: 0.7,
    bridge_power: 0.18,
    breakout_power: 0.5,
    deconstruction_potential: 0.28,
    backlash_risk: 0.46,
    position: { x: 178, y: 130 },
    visual_color: OPINION_STATE_COLORS.oppose,
    confidence: 0.68,
    parameter_source: PARAMETER_SOURCE,
  },
  {
    core_id: 'official',
    core_type: 'official_core',
    label: '官方说明',
    stance_label: '事实边界',
    stance_score: 0.66,
    source_type: 'official_statement',
    source_credibility: 0.76,
    evidence_strength: 0.64,
    logic_strength: 0.7,
    emotional_intensity: 0.26,
    extremity_score: 0.18,
    gravitational_pull: 0.12,
    neutral_acceptance: 0.68,
    same_camp_reinforcement: 0.48,
    opponent_resistance: 0.34,
    bridge_power: 0.42,
    breakout_power: 0.2,
    deconstruction_potential: 0.18,
    backlash_risk: 0.16,
    position: { x: 560, y: 150 },
    visual_color: '#42f5d7',
    confidence: 0.7,
    parameter_source: PARAMETER_SOURCE,
  },
  {
    core_id: 'third_party',
    core_type: 'explanation_core',
    label: '第三方解释',
    stance_label: '独立事实链',
    stance_score: 0.34,
    source_type: 'third_party_explanation',
    source_credibility: 0.7,
    evidence_strength: 0.66,
    logic_strength: 0.72,
    emotional_intensity: 0.24,
    extremity_score: 0.12,
    gravitational_pull: 0.08,
    neutral_acceptance: 0.72,
    same_camp_reinforcement: 0.32,
    opponent_resistance: 0.26,
    bridge_power: 0.62,
    breakout_power: 0.24,
    deconstruction_potential: 0.36,
    backlash_risk: 0.12,
    position: { x: 510, y: 386 },
    visual_color: '#78a6ff',
    confidence: 0.68,
    parameter_source: PARAMETER_SOURCE,
  },
  {
    core_id: 'deconstruction',
    core_type: 'deconstruction_core',
    label: '社区解构梗',
    stance_label: '叙事降压',
    stance_score: 0.08,
    source_type: 'community_reframe',
    source_credibility: 0.52,
    evidence_strength: 0.36,
    logic_strength: 0.42,
    emotional_intensity: 0.42,
    extremity_score: 0.2,
    gravitational_pull: 0.04,
    neutral_acceptance: 0.74,
    same_camp_reinforcement: 0.3,
    opponent_resistance: 0.22,
    bridge_power: 0.76,
    breakout_power: 0.18,
    deconstruction_potential: 0.68,
    backlash_risk: 0.18,
    position: { x: 266, y: 380 },
    visual_color: OPINION_STATE_COLORS.bridge,
    confidence: 0.64,
    parameter_source: PARAMETER_SOURCE,
  },
]

const BASE_CAMP_DYNAMICS = {
  conversion_score: 0.18,
  neutralization_score: 0.16,
  withdrawal_score: 0.12,
  hardening_score: 0.16,
  backlash_score: 0.14,
  reactivation_risk: 0.24,
  parameter_source: PARAMETER_SOURCE,
}

const BASE_DECONSTRUCTION_CORE = {
  core_id: 'deconstruction',
  label: '社区解构梗',
  deconstruction_type: 'symbolic_deflation',
  target_core_id: 'opposition',
  threat_deflation: 0.24,
  humor_acceptance: 0.42,
  face_saving_score: 0.5,
  neutralization_power: 0.2,
  conversion_power: 0.1,
  withdrawal_power: 0.16,
  ridicule_persistence: 0.24,
  meme_replicability: 0.36,
  community_co_creation: 0.42,
  backlash_risk: 0.18,
  long_term_stigma_risk: 0.14,
  deconstruction_fit_score: 0.28,
  confidence: 0.62,
  parameter_source: PARAMETER_SOURCE,
}

const BASE_RESPONSE_TEMPO = {
  clarification_priority: 0.42,
  faq_priority: 0.36,
  third_party_explanation_priority: 0.28,
  deconstruction_window_score: 0.08,
  wait_and_monitor_score: 0.46,
  recommendation_label: '观察后补充事实',
  recommendation_text: '当前更适合补充事实说明，不建议把静态 mock 推演解读为因果结论。',
  risk_notes: ['低置信度 mock，仅用于前端视觉原型。'],
  parameter_source: PARAMETER_SOURCE,
}

const BASE_REPUTATION_MEMORY = {
  unresolved_grievance_score: 0.22,
  stigma_persistence: 0.24,
  meme_persistence: 0.18,
  trust_recovery: 0.42,
  reactivation_risk: 0.24,
  monitoring_notes: ['退出讨论不等于问题解决，仍需人工复核来源与语境。'],
  parameter_source: PARAMETER_SOURCE,
}

export const SCENARIO_CONFIGS = {
  natural: {
    label: '自然演化',
    responseLabel: '观察后补充事实',
    responseText: '当前更适合补充事实说明，避免把静态 mock 变化解释成因果确定。',
    echo_chamber_score: 0.58,
    saturation_ratio: 0.62,
    fatigue_rate: 0.22,
    breakout_risk: 0.32,
    neutralization_score: 0.16,
    withdrawal_score: 0.12,
    backlash_score: 0.14,
    hardening_score: 0.16,
    deconstruction_window_score: 0.08,
    unresolved_grievance_score: 0.22,
    reactivation_risk: 0.24,
    deconstructionFit: 0.28,
    pull: { opposition: 0.42, official: 0.12, third_party: 0.08, deconstruction: 0.04 },
  },
  official_clarification: {
    label: '官方澄清',
    responseLabel: '先给事实边界',
    responseText: '温和反对者存在中立化窗口，适合发布可核验事实说明与更新时间。',
    echo_chamber_score: 0.48,
    saturation_ratio: 0.5,
    fatigue_rate: 0.18,
    breakout_risk: 0.24,
    neutralization_score: 0.34,
    withdrawal_score: 0.16,
    backlash_score: 0.12,
    hardening_score: 0.12,
    deconstruction_window_score: 0.12,
    unresolved_grievance_score: 0.18,
    reactivation_risk: 0.18,
    deconstructionFit: 0.22,
    pull: { opposition: 0.28, official: 0.42, third_party: 0.14, deconstruction: 0.08 },
  },
  faq_explainer: {
    label: 'FAQ / 长文解释',
    responseLabel: '降低重复误解',
    responseText: '重复疑问较多时，FAQ 比高频短回应更能降低回音壁饱和度。',
    echo_chamber_score: 0.43,
    saturation_ratio: 0.46,
    fatigue_rate: 0.2,
    breakout_risk: 0.18,
    neutralization_score: 0.42,
    withdrawal_score: 0.18,
    backlash_score: 0.1,
    hardening_score: 0.1,
    deconstruction_window_score: 0.2,
    unresolved_grievance_score: 0.16,
    reactivation_risk: 0.16,
    deconstructionFit: 0.3,
    pull: { opposition: 0.24, official: 0.3, third_party: 0.34, deconstruction: 0.14 },
  },
  third_party_explanation: {
    label: '第三方说明',
    responseLabel: '独立事实链辅助',
    responseText: '第三方说明适合承接事实争议，但仍需保留人工复核和来源说明。',
    echo_chamber_score: 0.4,
    saturation_ratio: 0.44,
    fatigue_rate: 0.18,
    breakout_risk: 0.2,
    neutralization_score: 0.38,
    withdrawal_score: 0.16,
    backlash_score: 0.1,
    hardening_score: 0.1,
    deconstruction_window_score: 0.24,
    unresolved_grievance_score: 0.15,
    reactivation_risk: 0.16,
    deconstructionFit: 0.34,
    pull: { opposition: 0.2, official: 0.16, third_party: 0.48, deconstruction: 0.18 },
  },
  community_deconstruction: {
    label: '社区解构',
    responseLabel: '轻量叙事降压',
    responseText: '当 EchoBox 高热但外溢较弱时，轻量解构可降低冲突表达强度。',
    echo_chamber_score: 0.36,
    saturation_ratio: 0.42,
    fatigue_rate: 0.28,
    breakout_risk: 0.16,
    neutralization_score: 0.44,
    withdrawal_score: 0.28,
    backlash_score: 0.08,
    hardening_score: 0.08,
    deconstruction_window_score: 0.54,
    unresolved_grievance_score: 0.14,
    reactivation_risk: 0.14,
    deconstructionFit: 0.58,
    pull: { opposition: 0.18, official: 0.14, third_party: 0.2, deconstruction: 0.56 },
  },
  delayed_response: {
    label: '延迟回应',
    responseLabel: '补充阶段性说明',
    responseText: '声量下降不等于问题解决，延迟回应下潜伏不满和反噬风险会积累。',
    echo_chamber_score: 0.72,
    saturation_ratio: 0.76,
    fatigue_rate: 0.12,
    breakout_risk: 0.48,
    neutralization_score: 0.08,
    withdrawal_score: 0.1,
    backlash_score: 0.34,
    hardening_score: 0.32,
    deconstruction_window_score: 0.04,
    unresolved_grievance_score: 0.42,
    reactivation_risk: 0.46,
    deconstructionFit: 0.1,
    pull: { opposition: 0.58, official: 0.04, third_party: 0.04, deconstruction: 0.02 },
  },
  no_response: {
    label: '无回应',
    responseLabel: '仅作基线对照',
    responseText: '无回应基线下，潜伏不满与破圈风险会持续累积，不建议作为长期策略。',
    echo_chamber_score: 0.8,
    saturation_ratio: 0.82,
    fatigue_rate: 0.08,
    breakout_risk: 0.58,
    neutralization_score: 0.04,
    withdrawal_score: 0.08,
    backlash_score: 0.48,
    hardening_score: 0.44,
    deconstruction_window_score: 0.02,
    unresolved_grievance_score: 0.58,
    reactivation_risk: 0.56,
    deconstructionFit: 0.04,
    pull: { opposition: 0.66, official: 0.02, third_party: 0.02, deconstruction: 0.01 },
  },
}

export const SCENARIO_OPTIONS = Object.entries(SCENARIO_CONFIGS).map(([value, scenario]) => ({
  value,
  label: scenario.label,
}))

function seededRandom(seed) {
  let value = seed % 2147483647
  if (value <= 0) value += 2147483646
  return () => {
    value = (value * 16807) % 2147483647
    return (value - 1) / 2147483646
  }
}

function clone(value) {
  return JSON.parse(JSON.stringify(value))
}

export function clamp01(value) {
  if (!Number.isFinite(Number(value))) return 0
  return Math.max(0, Math.min(1, Number(value)))
}

export function scoreToPercent(value) {
  return Math.round(clamp01(value) * 100)
}

export function campStateToVisual(campState, cluster = {}) {
  if (cluster.bridge_power > 0.74 && campState !== 'withdrawn') {
    return { key: 'bridge', label: '桥接人群簇', color: OPINION_STATE_COLORS.bridge }
  }
  return CAMP_STATE_VISUALS[campState] || CAMP_STATE_VISUALS.neutral_observing
}

function initialCampState(roll) {
  if (roll < 0.12) return 'support_core'
  if (roll < 0.22) return 'support_soft'
  if (roll < 0.42) return 'neutral_observing'
  if (roll < 0.5) return 'neutral_engaged'
  if (roll < 0.7) return 'oppose_soft'
  if (roll < 0.82) return 'oppose_core'
  if (roll < 0.9) return 'dormant_grievance'
  return 'neutral_engaged'
}

function stanceFromCampState(campState, random) {
  if (campState.startsWith('support')) return 0.34 + random() * 0.5
  if (campState.startsWith('oppose')) return -0.78 + random() * 0.34
  if (campState === 'dormant_grievance') return -0.3 + random() * 0.18
  if (campState === 'withdrawn') return 0
  return -0.14 + random() * 0.28
}

export function buildMockPeopleClusters(seed = 20260613) {
  const random = seededRandom(seed)
  return Array.from({ length: PEOPLE_CLUSTER_COUNT }, (_, index) => {
    const campState = initialCampState(random())
    const influenceWeight = 0.18 + random() * 0.78
    const bridgePower = campState === 'neutral_engaged' && random() > 0.68 ? 0.76 + random() * 0.18 : random() * 0.56
    const stanceScore = stanceFromCampState(campState, random)
    return {
      cluster_id: `people_cluster_${String(index + 1).padStart(3, '0')}`,
      label: `匿名人群簇 ${index + 1}`,
      camp_state: bridgePower > 0.74 ? 'neutral_engaged' : campState,
      stance_label: stanceScore > 0.28 ? '支持倾向' : stanceScore < -0.28 ? '反对倾向' : '中立 / 摇摆',
      stance_score: Number(stanceScore.toFixed(3)),
      stance_strength: clamp01(Math.abs(stanceScore)),
      population_weight: clamp01(0.22 + random() * 0.72),
      mobility: clamp01(0.2 + random() * 0.7),
      identity_lock: clamp01(0.12 + random() * 0.78),
      evidence_sensitivity: clamp01(0.22 + random() * 0.72),
      emotion_load: clamp01(0.18 + random() * 0.76),
      fatigue: clamp01(random() * 0.28),
      grievance_memory: campState === 'dormant_grievance' ? clamp01(0.54 + random() * 0.34) : clamp01(random() * 0.48),
      deconstruction_receptivity: clamp01(0.22 + random() * 0.72),
      social_cost_to_switch: clamp01(0.18 + random() * 0.72),
      influence_weight: clamp01(influenceWeight),
      activity_weight: clamp01(0.24 + random() * 0.72),
      expression_intensity: clamp01(0.26 + random() * 0.7),
      bridge_power: clamp01(bridgePower),
      position: {
        x: 52 + random() * (BOX_WIDTH - 104),
        y: 50 + random() * (BOX_HEIGHT - 100),
      },
      velocity: {
        x: (random() - 0.5) * 0.72,
        y: (random() - 0.5) * 0.72,
      },
      confidence: clamp01(0.52 + random() * 0.36),
      parameter_source: PARAMETER_SOURCE,
      phase: random() * Math.PI * 2,
    }
  })
}

export function createOpinionEcosystemMock(seed = 20260613) {
  return {
    echoBox: clone(BASE_ECHO_BOX),
    influenceCores: clone(BASE_INFLUENCE_CORES),
    peopleClusters: buildMockPeopleClusters(seed),
    campDynamics: clone(BASE_CAMP_DYNAMICS),
    deconstructionCore: clone(BASE_DECONSTRUCTION_CORE),
    responseTempo: clone(BASE_RESPONSE_TEMPO),
    reputationMemory: clone(BASE_REPUTATION_MEMORY),
  }
}

export function applyMockScenario(baseScenario, scenarioKey) {
  const config = SCENARIO_CONFIGS[scenarioKey] || SCENARIO_CONFIGS.natural
  const next = clone(baseScenario)
  next.scenarioKey = scenarioKey
  next.scenarioLabel = config.label

  next.echoBox.echo_chamber_score = clamp01(config.echo_chamber_score)
  next.echoBox.saturation_ratio = clamp01(config.saturation_ratio)
  next.echoBox.fatigue_rate = clamp01(config.fatigue_rate)
  next.echoBox.breakout_risk = clamp01(config.breakout_risk)
  next.echoBox.internal_reinforcement = clamp01(config.echo_chamber_score * 0.78 + config.hardening_score * 0.22)
  next.echoBox.permeability_score = clamp01(1 - config.echo_chamber_score * 0.62)

  next.campDynamics.neutralization_score = clamp01(config.neutralization_score)
  next.campDynamics.withdrawal_score = clamp01(config.withdrawal_score)
  next.campDynamics.backlash_score = clamp01(config.backlash_score)
  next.campDynamics.hardening_score = clamp01(config.hardening_score)
  next.campDynamics.conversion_score = clamp01(config.neutralization_score * 0.46 + config.deconstruction_window_score * 0.2)
  next.campDynamics.reactivation_risk = clamp01(config.reactivation_risk)

  next.deconstructionCore.threat_deflation = clamp01(config.deconstructionFit * 0.76)
  next.deconstructionCore.humor_acceptance = clamp01(config.deconstructionFit * 0.82)
  next.deconstructionCore.neutralization_power = clamp01(config.deconstruction_window_score * 0.8)
  next.deconstructionCore.withdrawal_power = clamp01(config.withdrawal_score)
  next.deconstructionCore.backlash_risk = clamp01(config.backlash_score)
  next.deconstructionCore.deconstruction_fit_score = clamp01(config.deconstructionFit)
  next.deconstructionCore.meme_replicability = clamp01(config.deconstructionFit * 0.72 + 0.08)

  next.responseTempo.deconstruction_window_score = clamp01(config.deconstruction_window_score)
  next.responseTempo.clarification_priority = clamp01(config.pull.official * 0.86 + config.neutralization_score * 0.32)
  next.responseTempo.faq_priority = clamp01(config.pull.third_party * 0.7 + config.neutralization_score * 0.42)
  next.responseTempo.third_party_explanation_priority = clamp01(config.pull.third_party)
  next.responseTempo.wait_and_monitor_score = clamp01(0.62 - config.breakout_risk * 0.54)
  next.responseTempo.recommendation_label = config.responseLabel
  next.responseTempo.recommendation_text = config.responseText
  next.responseTempo.risk_notes = [
    '静态 mock 只用于原型演示，不代表因果确定。',
    config.backlash_score > 0.3 ? '反噬风险较高，建议保留人工复核。' : '仍需结合来源和上下文判断。',
  ]

  next.reputationMemory.unresolved_grievance_score = clamp01(config.unresolved_grievance_score)
  next.reputationMemory.reactivation_risk = clamp01(config.reactivation_risk)
  next.reputationMemory.stigma_persistence = clamp01(config.unresolved_grievance_score * 0.72 + config.hardening_score * 0.24)
  next.reputationMemory.meme_persistence = clamp01(config.deconstructionFit * 0.36 + config.backlash_score * 0.18)
  next.reputationMemory.trust_recovery = clamp01(0.62 - config.unresolved_grievance_score * 0.5 + config.neutralization_score * 0.22)

  next.influenceCores = next.influenceCores.map((core) => ({
    ...core,
    gravitational_pull: clamp01(config.pull[core.core_id] ?? core.gravitational_pull),
    neutral_acceptance: clamp01(core.neutral_acceptance + config.neutralization_score * 0.18),
    backlash_risk: clamp01(core.backlash_risk + config.backlash_score * 0.16),
  }))

  return next
}

export function computeCampDistribution(peopleClusters) {
  const campStates = peopleClusters.reduce((acc, cluster) => {
    acc[cluster.camp_state] = (acc[cluster.camp_state] || 0) + 1
    return acc
  }, {})
  const visualCounts = peopleClusters.reduce(
    (acc, cluster) => {
      const visual = campStateToVisual(cluster.camp_state, cluster)
      acc[visual.key] = (acc[visual.key] || 0) + 1
      return acc
    },
    { support: 0, neutral: 0, oppose: 0, uncertain: 0, bridge: 0, withdrawn: 0 },
  )

  return { campStates, visualCounts }
}

export function computeMockMetrics(echoBox, influenceCores, peopleClusters, responseTempo, reputationMemory) {
  const distribution = computeCampDistribution(peopleClusters)
  const activeClusters = peopleClusters.filter((cluster) => cluster.camp_state !== 'withdrawn')
  const activeCount = Math.max(1, activeClusters.length)
  const activeIntensity =
    activeClusters.reduce((sum, cluster) => sum + cluster.expression_intensity * cluster.activity_weight, 0) / activeCount
  const oppositionShare = distribution.visualCounts.oppose / Math.max(1, peopleClusters.length)
  const neutralShare =
    (distribution.visualCounts.neutral + distribution.visualCounts.uncertain + distribution.visualCounts.bridge) /
    Math.max(1, peopleClusters.length)
  const strongestCore = influenceCores.reduce((strongest, core) => {
    if (!strongest || core.gravitational_pull > strongest.gravitational_pull) return core
    return strongest
  }, null)

  return {
    counts: distribution.visualCounts,
    campDistribution: distribution.campStates,
    withdrawnShare: distribution.visualCounts.withdrawn / Math.max(1, peopleClusters.length),
    dormantGrievanceRisk: clamp01(reputationMemory.unresolved_grievance_score * 0.7 + oppositionShare * 0.52),
    echoBoxSaturation: clamp01(echoBox.saturation_ratio * 0.62 + activeIntensity * 0.38),
    breakoutRisk: clamp01(echoBox.breakout_risk * 0.68 + oppositionShare * 0.44),
    deconstructionWindow: clamp01(responseTempo.deconstruction_window_score * 0.72 + neutralShare * 0.28),
    responseTempo: responseTempo.recommendation_label,
    strongestCore,
  }
}

export function scenarioTargetForCluster(cluster, scenario) {
  if (cluster.camp_state === 'withdrawn') return null
  const cores = new Map(scenario.influenceCores.map((core) => [core.core_id, core]))
  const campState = cluster.camp_state
  const pull = {
    opposition: cores.get('opposition')?.gravitational_pull || 0,
    official: cores.get('official')?.gravitational_pull || 0,
    third_party: cores.get('third_party')?.gravitational_pull || 0,
    deconstruction: cores.get('deconstruction')?.gravitational_pull || 0,
  }

  if (campState.startsWith('oppose')) {
    if (pull.deconstruction > 0.3 && cluster.deconstruction_receptivity > 0.35) return cores.get('deconstruction')
    if (pull.official > pull.opposition && cluster.evidence_sensitivity > 0.35) return cores.get('official')
    if (pull.third_party > 0.28) return cores.get('third_party')
    return cores.get('opposition')
  }
  if (campState.startsWith('support')) return cores.get('official')
  if (cluster.bridge_power > 0.74) return pull.deconstruction > 0.25 ? cores.get('deconstruction') : cores.get('third_party')
  if (campState === 'dormant_grievance') return cores.get('opposition')
  if (campState === 'neutral_observing') return pull.third_party > pull.official ? cores.get('third_party') : cores.get('official')
  return scenario.campDynamics.neutralization_score > 0.35 ? cores.get('third_party') : cores.get('deconstruction')
}

function mutateClusterState(cluster, scenario, tick) {
  if (cluster.camp_state === 'withdrawn') return
  const gate = Math.abs(Math.sin((tick + cluster.phase * 100 + cluster.cluster_id.length) * 0.013))
  const dynamics = scenario.campDynamics

  if (cluster.camp_state.startsWith('oppose') && dynamics.neutralization_score > 0.28 && gate > 0.996) {
    cluster.camp_state = scenario.deconstructionCore.deconstruction_fit_score > 0.35 ? 'neutral_engaged' : 'neutral_observing'
    cluster.expression_intensity *= 0.74
  } else if (cluster.camp_state === 'dormant_grievance' && dynamics.backlash_score > 0.3 && gate > 0.996) {
    cluster.camp_state = 'oppose_soft'
    cluster.expression_intensity = clamp01(cluster.expression_intensity + 0.12)
  } else if (cluster.camp_state === 'neutral_observing' && dynamics.neutralization_score > 0.32 && gate > 0.994) {
    cluster.camp_state = 'neutral_engaged'
    cluster.expression_intensity *= 0.84
  } else if (cluster.camp_state === 'neutral_engaged' && dynamics.conversion_score > 0.28 && gate > 0.997) {
    cluster.camp_state = 'support_soft'
  } else if (cluster.camp_state.startsWith('support') && scenario.echoBox.breakout_risk > 0.45 && gate > 0.998) {
    cluster.camp_state = 'neutral_observing'
  }

  cluster.fatigue = clamp01(cluster.fatigue + scenario.echoBox.fatigue_rate * 0.0009)
  cluster.expression_intensity = clamp01(
    Math.max(
      0.12,
      cluster.expression_intensity +
        dynamics.hardening_score * 0.0007 -
        scenario.deconstructionCore.deconstruction_fit_score * 0.0006,
    ),
  )

  if (cluster.fatigue > 0.86 && gate > 0.992) {
    cluster.camp_state = 'withdrawn'
    cluster.expression_intensity *= 0.42
  }
}

export function stepPeopleClusters(peopleClusters, scenario, tick) {
  peopleClusters.forEach((cluster) => {
    mutateClusterState(cluster, scenario, tick)
    if (cluster.camp_state === 'withdrawn') {
      cluster.velocity.x *= 0.985
      cluster.velocity.y *= 0.985
    }
    const target = scenarioTargetForCluster(cluster, scenario)
    if (target) {
      const dx = target.position.x - cluster.position.x
      const dy = target.position.y - cluster.position.y
      const distance = Math.max(24, Math.hypot(dx, dy))
      const pullScale = (target.gravitational_pull + cluster.mobility * 0.08 + 0.05) * 0.004
      cluster.velocity.x += (dx / distance) * pullScale
      cluster.velocity.y += (dy / distance) * pullScale
    }
    cluster.velocity.x += Math.sin(tick * 0.015 + cluster.phase) * 0.0022
    cluster.velocity.y += Math.cos(tick * 0.012 + cluster.phase) * 0.002
    const maxSpeed = 0.24 + cluster.activity_weight * 0.62
    const speed = Math.hypot(cluster.velocity.x, cluster.velocity.y)
    if (speed > maxSpeed) {
      cluster.velocity.x = (cluster.velocity.x / speed) * maxSpeed
      cluster.velocity.y = (cluster.velocity.y / speed) * maxSpeed
    }
    cluster.position.x += cluster.velocity.x
    cluster.position.y += cluster.velocity.y
    if (cluster.position.x < 28 || cluster.position.x > BOX_WIDTH - 28) {
      cluster.velocity.x *= -0.9
      cluster.position.x = Math.min(BOX_WIDTH - 28, Math.max(28, cluster.position.x))
    }
    if (cluster.position.y < 28 || cluster.position.y > BOX_HEIGHT - 28) {
      cluster.velocity.y *= -0.9
      cluster.position.y = Math.min(BOX_HEIGHT - 28, Math.max(28, cluster.position.y))
    }
    cluster.velocity.x *= 0.992
    cluster.velocity.y *= 0.992
  })
}
