import {
  BOX_HEIGHT,
  BOX_WIDTH,
  clamp01,
  computeCampDistribution,
} from './opinionEcosystemMock.js'

const PARAMETER_SOURCE = 'frontend_evidence_fixture_mapper_v1'

const CORE_POSITIONS = {
  opposition: { x: 178, y: 130 },
  official: { x: 560, y: 150 },
  third_party: { x: 510, y: 386 },
  deconstruction: { x: 266, y: 380 },
  neutral_analysis: { x: 392, y: 258 },
}

const CORE_COLORS = {
  opposition: '#ff5d8f',
  official: '#42f5d7',
  third_party: '#78a6ff',
  deconstruction: '#a478ff',
  neutral_analysis: '#f5c44b',
}

const TRUST_WEIGHT = {
  high: 0.9,
  medium: 0.72,
  medium_low: 0.52,
  low: 0.32,
  unverified: 0.18,
}

const REVIEW_WEIGHT = {
  approved: 1,
  not_reviewed: 0.72,
  review_needed: 0.48,
  marked_weak: 0.42,
  rejected: 0,
}

const PROVENANCE_WEIGHT = {
  mock_fixture: 0.72,
  manual_url: 0.58,
  user_upload: 0.48,
  data_vendor: 0.5,
}

const ROOT_EVIDENCE_TYPES = [
  'video',
  'post',
  'article',
  'official_statement',
  'third_party_explanation',
  'meme',
  'community_discussion',
  'media_article',
  'community_meme',
]

function numeric(value, fallback = 0) {
  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : fallback
}

function activeEvidence(evidenceItems) {
  return evidenceItems.filter((item) => item.review_status !== 'rejected')
}

function uniqueByDuplicateGroup(evidenceItems) {
  const seen = new Set()
  return evidenceItems.filter((item) => {
    const key = item.duplicate_group_id || item.content_hash || item.evidence_id
    if (seen.has(key)) return false
    seen.add(key)
    return true
  })
}

function childCount(rootId, evidenceItems) {
  return evidenceItems.filter((item) => item.root_id === rootId && ['comment', 'reply'].includes(item.evidence_type)).length
}

function textOf(evidence) {
  return [evidence.title, evidence.body_text, evidence.comment_text].filter(Boolean).join(' ')
}

function classifyStance(evidence) {
  const stanceHint = String(evidence.stance_hint || '').toLowerCase()
  const campHint = String(evidence.camp_state_hint || '').toLowerCase()
  if (['opposed', 'oppose', 'opposition', 'against', 'critical'].includes(stanceHint)) {
    return campHint === 'mobilizing' ? -0.72 : -0.46
  }
  if (['supporting', 'support', 'supportive', 'for'].includes(stanceHint)) {
    return campHint === 'cooling' ? 0.42 : 0.36
  }
  if (['neutral', 'observing', 'unknown'].includes(stanceHint)) {
    return 0.04
  }

  const text = textOf(evidence)
  const supportHits = ['可以先观望', '接受', '放心', '合理', '降下来', '解释比较清楚', '更容易接受']
  const opposeHits = ['太慢', '失去意义', '不想讨论', '信任恢复', '重新提起', '没有看到来源', '只玩梗']
  const support = supportHits.reduce((score, hit) => score + (text.includes(hit) ? 1 : 0), 0)
  const oppose = opposeHits.reduce((score, hit) => score + (text.includes(hit) ? 1 : 0), 0)
  if (oppose > support) return -clamp01(0.28 + oppose * 0.18)
  if (support > oppose) return clamp01(0.22 + support * 0.18)
  return text.includes('观望') || text.includes('等待') || text.includes('整理') ? 0.04 : 0
}

function coreIdForEvidence(evidence) {
  if (evidence.evidence_type === 'official_statement') return 'official'
  if (['third_party_explanation', 'media_article', 'article'].includes(evidence.evidence_type)) return 'third_party'
  if (['meme', 'community_meme'].includes(evidence.evidence_type)) return 'deconstruction'
  if (['post', 'community_discussion'].includes(evidence.evidence_type)) return 'neutral_analysis'
  return 'opposition'
}

function coreTypeForEvidence(evidence) {
  if (evidence.evidence_type === 'official_statement') return 'official_statement'
  if (['third_party_explanation', 'media_article', 'article'].includes(evidence.evidence_type)) return 'media_article'
  if (['meme', 'community_meme'].includes(evidence.evidence_type)) return 'community_meme'
  if (['post', 'community_discussion'].includes(evidence.evidence_type)) return 'forum_thread'
  return 'creator_video'
}

function scenarioSeed(index) {
  return {
    x: 72 + ((index * 67) % (BOX_WIDTH - 144)),
    y: 64 + ((index * 91) % (BOX_HEIGHT - 128)),
  }
}

export function computeEvidenceConfidence(evidence) {
  if (evidence.review_status === 'rejected') return 0
  const trustBase = TRUST_WEIGHT[evidence.trust_label] ?? 0.4
  const reviewBase = REVIEW_WEIGHT[evidence.review_status] ?? 0.5
  const provenanceBase = PROVENANCE_WEIGHT[evidence.provenance_type] ?? 0.4
  const declaredTrust = clamp01(evidence.trust_score ?? trustBase)
  const duplicatePenalty = evidence.duplicate_group_id ? 0.88 : 1
  const riskPenalty = Math.max(0.42, 1 - (evidence.risk_flags || []).length * 0.1)
  return clamp01((trustBase * 0.34 + declaredTrust * 0.36 + reviewBase * 0.18 + provenanceBase * 0.12) * duplicatePenalty * riskPenalty)
}

export function classifyEvidenceRole(evidence) {
  if (evidence.review_status === 'rejected') {
    return {
      evidence_id: evidence.evidence_id,
      role: 'unknown_or_unusable',
      role_confidence: 0,
      role_reason: 'rejected evidence is excluded from active mock weights',
    }
  }

  if (evidence.evidence_type === 'meme') {
    return {
      evidence_id: evidence.evidence_id,
      role: 'deconstruction_candidate',
      role_confidence: computeEvidenceConfidence(evidence),
      role_reason: 'meme evidence can become a deconstruction core candidate',
    }
  }

  if (ROOT_EVIDENCE_TYPES.includes(evidence.evidence_type)) {
    return {
      evidence_id: evidence.evidence_id,
      role: 'candidate_influence_core',
      role_confidence: computeEvidenceConfidence(evidence),
      role_reason: 'root content can become an influence core in the local mock mapping',
    }
  }

  if (['comment', 'reply'].includes(evidence.evidence_type)) {
    return {
      evidence_id: evidence.evidence_id,
      role: 'people_expression',
      role_confidence: computeEvidenceConfidence(evidence),
      role_reason: 'comment or reply maps to anonymous PeopleCluster groups',
    }
  }

  return {
    evidence_id: evidence.evidence_id,
    role: 'supporting_reference',
    role_confidence: computeEvidenceConfidence(evidence),
    role_reason: 'supporting reference for mapped ecosystem objects',
  }
}

export function buildSourceIdentities(evidenceItems) {
  const activeItems = activeEvidence(evidenceItems)
  const bySource = new Map()
  activeItems.forEach((evidence) => {
    const key = `${evidence.platform || 'mock'}:${evidence.author_id || evidence.author_name || 'anonymous'}`
    if (!bySource.has(key)) {
      bySource.set(key, {
        source_id: `source_${bySource.size + 1}`,
        case_id: evidence.case_id,
        platform: evidence.platform,
        source_type:
          evidence.evidence_type === 'official_statement'
            ? 'official'
            : evidence.evidence_type === 'third_party_explanation'
              ? 'expert'
              : evidence.evidence_type === 'video'
                ? 'creator'
                : 'ordinary_user',
        platform_source_hash: `mock_hash_${bySource.size + 1}`,
        display_label_policy: {
          public_label: evidence.evidence_type === 'official_statement' ? '虚构官方来源' : `匿名来源 ${bySource.size + 1}`,
          show_public_name: false,
          anonymize_in_public_demo: true,
        },
        credibility: {
          source_credibility: computeEvidenceConfidence(evidence),
          credibility_confidence: 0.62,
          parameter_source: PARAMETER_SOURCE,
        },
        evidence_ids: [],
      })
    }
    bySource.get(key).evidence_ids.push(evidence.evidence_id)
  })
  return Array.from(bySource.values())
}

export function buildInfluenceCores(evidenceItems) {
  const coreCandidates = activeEvidence(evidenceItems).filter((evidence) => ROOT_EVIDENCE_TYPES.includes(evidence.evidence_type))

  return coreCandidates.map((evidence) => {
    const coreId = coreIdForEvidence(evidence)
    const confidence = computeEvidenceConfidence(evidence)
    const interactions = numeric(evidence.like_count) + numeric(evidence.reply_count) * 2 + numeric(evidence.share_count) * 3
    const attentionWeight = clamp01(Math.log10(10 + numeric(evidence.view_count) + interactions * 8) / 5)
    const stanceScore =
      coreId === 'opposition' ? -0.72 : coreId === 'official' ? 0.66 : coreId === 'third_party' ? 0.34 : coreId === 'deconstruction' ? 0.08 : 0.04
    return {
      core_id: coreId,
      source_evidence_id: evidence.evidence_id,
      core_type: coreTypeForEvidence(evidence),
      label: evidence.title,
      stance_label: stanceScore > 0.2 ? 'support' : stanceScore < -0.2 ? 'oppose' : 'neutral',
      stance_score: stanceScore,
      source_type: evidence.source_type,
      source_credibility: confidence,
      evidence_strength: clamp01(confidence * 0.72 + attentionWeight * 0.18),
      logic_strength: clamp01(coreId === 'third_party' || coreId === 'official' ? 0.68 + confidence * 0.18 : 0.42 + confidence * 0.18),
      emotional_intensity: clamp01(coreId === 'opposition' ? 0.72 : coreId === 'deconstruction' ? 0.42 : 0.26),
      extremity_score: clamp01(coreId === 'opposition' ? 0.62 : coreId === 'deconstruction' ? 0.2 : 0.12),
      gravitational_pull: clamp01(attentionWeight * 0.55 + childCount(evidence.evidence_id, evidenceItems) * 0.035 + confidence * 0.22),
      neutral_acceptance: clamp01(coreId === 'official' || coreId === 'third_party' ? 0.62 + confidence * 0.18 : coreId === 'deconstruction' ? 0.7 : 0.2),
      same_camp_reinforcement: clamp01(coreId === 'opposition' ? 0.7 : 0.34 + attentionWeight * 0.18),
      opponent_resistance: clamp01(coreId === 'opposition' ? 0.68 : 0.22 + confidence * 0.14),
      bridge_power: clamp01(coreId === 'third_party' ? 0.66 : coreId === 'deconstruction' ? 0.76 : coreId === 'official' ? 0.44 : 0.18),
      breakout_power: clamp01(coreId === 'opposition' ? 0.52 + attentionWeight * 0.18 : attentionWeight * 0.32),
      deconstruction_potential: clamp01(coreId === 'deconstruction' ? 0.72 : coreId === 'third_party' ? 0.36 : 0.24),
      backlash_risk: clamp01(coreId === 'opposition' ? 0.44 : coreId === 'deconstruction' ? 0.24 : 0.16),
      position: CORE_POSITIONS[coreId],
      visual_color: CORE_COLORS[coreId],
      confidence,
      parameter_source: PARAMETER_SOURCE,
    }
  })
}

export function buildEchoBoxes(evidenceItems, influenceCores) {
  const activeItems = uniqueByDuplicateGroup(activeEvidence(evidenceItems))
  const comments = activeItems.filter((item) => ['comment', 'reply'].includes(item.evidence_type))
  const opposeSignals = comments.filter((item) => classifyStance(item) < -0.2).length
  const supportSignals = comments.filter((item) => classifyStance(item) > 0.2).length
  const neutralSignals = Math.max(0, comments.length - opposeSignals - supportSignals)
  const deconstructionCore = influenceCores.find((core) => core.core_id === 'deconstruction')
  const oppositionCore = influenceCores.find((core) => core.core_id === 'opposition')
  const echoChamberScore = clamp01(0.32 + opposeSignals / Math.max(1, comments.length) * 0.34 + (oppositionCore?.gravitational_pull || 0) * 0.26)
  const saturationRatio = clamp01(0.35 + comments.length / 36 + opposeSignals / Math.max(1, comments.length) * 0.24)

  return [
    {
      box_id: 'mapped_echo_box_main_community',
      case_id: evidenceItems[0]?.case_id || 'mock_case',
      label: '主社区回音壁',
      platform: 'mock_community',
      box_type: 'aggregate_box',
      echo_chamber_score: echoChamberScore,
      carrying_capacity: 1,
      saturation_ratio: saturationRatio,
      permeability_score: clamp01(0.26 + neutralSignals / Math.max(1, comments.length) * 0.44 + (deconstructionCore?.bridge_power || 0) * 0.18),
      internal_reinforcement: clamp01(echoChamberScore * 0.74 + opposeSignals / Math.max(1, comments.length) * 0.2),
      external_inflow_rate: clamp01(0.18 + influenceCores.length * 0.035),
      fatigue_rate: clamp01(0.16 + comments.filter((item) => textOf(item).includes('累') || textOf(item).includes('不想讨论')).length * 0.05),
      breakout_risk: clamp01((oppositionCore?.breakout_power || 0.2) * 0.6 + saturationRatio * 0.28),
      lifecycle_stage: saturationRatio > 0.72 ? 'plateau' : echoChamberScore > 0.58 ? 'peak' : 'rise',
      confidence: clamp01(activeItems.reduce((sum, item) => sum + computeEvidenceConfidence(item), 0) / Math.max(1, activeItems.length)),
      parameter_source: PARAMETER_SOURCE,
      influence_core_ids: influenceCores.map((core) => core.core_id),
      evidence_count: activeItems.length,
    },
  ]
}

export function buildPeopleClusters(evidenceItems, echoBoxes) {
  const expressions = uniqueByDuplicateGroup(activeEvidence(evidenceItems)).filter((item) => ['comment', 'reply'].includes(item.evidence_type))
  const buckets = [
    {
      cluster_id: 'mapped_cluster_oppose_core',
      label: '核心玩家反对群体',
      filter: (item) => classifyStance(item) < -0.5,
      camp_state: 'oppose_core',
    },
    {
      cluster_id: 'mapped_cluster_oppose_soft',
      label: '温和反对群体',
      filter: (item) => classifyStance(item) < -0.18 && classifyStance(item) >= -0.5,
      camp_state: 'oppose_soft',
    },
    {
      cluster_id: 'mapped_cluster_neutral_engaged',
      label: '证据敏感中立群体',
      filter: (item) => Math.abs(classifyStance(item)) <= 0.18 && (textOf(item).includes('解释') || textOf(item).includes('数据') || textOf(item).includes('整理')),
      camp_state: 'neutral_engaged',
    },
    {
      cluster_id: 'mapped_cluster_support_soft',
      label: '温和支持群体',
      filter: (item) => classifyStance(item) > 0.18,
      camp_state: 'support_soft',
    },
    {
      cluster_id: 'mapped_cluster_fatigue',
      label: '疲劳围观群体',
      filter: (item) => textOf(item).includes('不想讨论') || textOf(item).includes('累') || textOf(item).includes('等结果'),
      camp_state: 'withdrawn',
    },
    {
      cluster_id: 'mapped_cluster_dormant_grievance',
      label: '潜伏不满群体',
      filter: (item) => textOf(item).includes('重新提起') || textOf(item).includes('信任恢复') || textOf(item).includes('问题没有'),
      camp_state: 'dormant_grievance',
    },
  ]

  return buckets
    .map((bucket, index) => {
      const matched = expressions.filter(bucket.filter)
      if (!matched.length) return null
      const confidence = matched.reduce((sum, item) => sum + computeEvidenceConfidence(item), 0) / matched.length
      const stanceScore = matched.reduce((sum, item) => sum + classifyStance(item), 0) / matched.length
      const seed = scenarioSeed(index)
      const emotionLoad = clamp01(Math.abs(stanceScore) * 0.62 + matched.reduce((sum, item) => sum + numeric(item.like_count), 0) / 280)
      return {
        cluster_id: bucket.cluster_id,
        label: bucket.label,
        echo_box_id: echoBoxes[0]?.box_id,
        evidence_ids: matched.map((item) => item.evidence_id),
        camp_state: bucket.camp_state,
        stance_label: stanceScore > 0.18 ? 'support' : stanceScore < -0.18 ? 'oppose' : 'neutral',
        stance_score: Number(stanceScore.toFixed(3)),
        stance_strength: clamp01(Math.abs(stanceScore)),
        population_weight: clamp01(matched.length / Math.max(1, expressions.length) + 0.18),
        mobility: clamp01(bucket.camp_state.includes('soft') || bucket.camp_state.includes('neutral') ? 0.62 : 0.34),
        identity_lock: clamp01(bucket.camp_state.includes('core') ? 0.7 : 0.32 + Math.abs(stanceScore) * 0.36),
        evidence_sensitivity: clamp01(bucket.camp_state.includes('neutral') ? 0.78 : 0.36 + confidence * 0.24),
        emotion_load: emotionLoad,
        fatigue: clamp01(bucket.camp_state === 'withdrawn' ? 0.86 : 0.18 + matched.length * 0.02),
        grievance_memory: clamp01(bucket.camp_state === 'dormant_grievance' ? 0.82 : Math.abs(stanceScore) * 0.42),
        deconstruction_receptivity: clamp01(bucket.camp_state.includes('neutral') || bucket.camp_state.includes('soft') ? 0.62 : 0.28),
        social_cost_to_switch: clamp01(bucket.camp_state.includes('core') ? 0.74 : 0.36),
        influence_weight: clamp01(0.22 + matched.length / Math.max(1, expressions.length) * 0.8),
        activity_weight: clamp01(0.22 + matched.reduce((sum, item) => sum + numeric(item.reply_count), 0) / 28),
        expression_intensity: clamp01(0.28 + emotionLoad * 0.58),
        bridge_power: clamp01(bucket.camp_state === 'neutral_engaged' ? 0.82 : bucket.camp_state === 'support_soft' ? 0.42 : 0.18),
        position: seed,
        velocity: { x: (index % 2 === 0 ? 0.22 : -0.18) * (1 + index * 0.03), y: (index % 3 === 0 ? 0.16 : -0.14) },
        confidence: clamp01(confidence),
        parameter_source: PARAMETER_SOURCE,
        phase: index * 0.74,
      }
    })
    .filter(Boolean)
}

export function buildCampDynamics(echoBoxes, influenceCores, peopleClusters) {
  const distribution = computeCampDistribution(peopleClusters)
  const total = Math.max(1, peopleClusters.length)
  const opposeShare = distribution.visualCounts.oppose / total
  const neutralShare = (distribution.visualCounts.neutral + distribution.visualCounts.uncertain + distribution.visualCounts.bridge) / total
  const withdrawnShare = distribution.visualCounts.withdrawn / total
  const deconstruction = influenceCores.find((core) => core.core_id === 'deconstruction')
  const official = influenceCores.find((core) => core.core_id === 'official')
  const echoBox = echoBoxes[0]

  return {
    conversion_score: clamp01((official?.neutral_acceptance || 0) * 0.28 + neutralShare * 0.34),
    neutralization_score: clamp01((official?.gravitational_pull || 0) * 0.32 + (deconstruction?.bridge_power || 0) * 0.22 + neutralShare * 0.22),
    withdrawal_score: clamp01(withdrawnShare * 0.7 + (echoBox?.fatigue_rate || 0) * 0.38),
    hardening_score: clamp01(opposeShare * 0.44 + (echoBox?.internal_reinforcement || 0) * 0.32),
    backlash_score: clamp01((deconstruction?.backlash_risk || 0) * 0.32 + (echoBox?.breakout_risk || 0) * 0.28),
    reactivation_risk: clamp01(peopleClusters.filter((cluster) => cluster.camp_state === 'dormant_grievance').length / total + (echoBox?.breakout_risk || 0) * 0.38),
    parameter_source: PARAMETER_SOURCE,
  }
}

export function buildDeconstructionCores(evidenceItems, influenceCores) {
  const meme = activeEvidence(evidenceItems).find((item) => ['meme', 'community_meme'].includes(item.evidence_type))
  const deconstructionInfluence = influenceCores.find((core) => core.core_id === 'deconstruction')
  if (!meme) return []
  const confidence = computeEvidenceConfidence(meme)
  return [
    {
      core_id: 'deconstruction',
      label: meme.title || '社区解构梗',
      deconstruction_type: 'meme_reframe',
      target_core_id: 'opposition',
      threat_deflation: clamp01(confidence * 0.42),
      humor_acceptance: clamp01(0.38 + confidence * 0.42),
      face_saving_score: clamp01(0.44 + confidence * 0.32),
      neutralization_power: clamp01((deconstructionInfluence?.bridge_power || 0.4) * 0.56),
      conversion_power: clamp01(confidence * 0.22),
      withdrawal_power: clamp01(0.18 + confidence * 0.22),
      ridicule_persistence: clamp01(0.2 + numeric(meme.share_count) / 220),
      meme_replicability: clamp01(0.32 + numeric(meme.share_count) / 120),
      community_co_creation: clamp01(0.34 + numeric(meme.reply_count) / 100),
      backlash_risk: clamp01(0.16 + (meme.risk_flags || []).length * 0.08),
      long_term_stigma_risk: clamp01(0.12 + numeric(meme.share_count) / 380),
      deconstruction_fit_score: clamp01(0.24 + confidence * 0.46),
      confidence,
      parameter_source: PARAMETER_SOURCE,
    },
  ]
}

export function buildResponseTempo(echoBoxes, influenceCores, peopleClusters, campDynamics, deconstructionCores) {
  const echoBox = echoBoxes[0]
  const deconstruction = deconstructionCores[0]
  const official = influenceCores.find((core) => core.core_id === 'official')
  const thirdParty = influenceCores.find((core) => core.core_id === 'third_party')
  const distribution = computeCampDistribution(peopleClusters)
  const neutralShare =
    (distribution.visualCounts.neutral + distribution.visualCounts.uncertain + distribution.visualCounts.bridge) / Math.max(1, peopleClusters.length)
  const deconstructionWindow = clamp01((deconstruction?.deconstruction_fit_score || 0) * 0.46 + neutralShare * 0.34 - campDynamics.backlash_score * 0.18)

  let recommendation_label = '补充事实说明'
  let recommendation_text = '当前更适合补充事实说明，不建议强行解构。'
  if (campDynamics.reactivation_risk > 0.42) {
    recommendation_label = '关注潜伏反噬'
    recommendation_text = '声量下降不等于问题解决，存在潜伏反噬风险。'
  } else if (deconstructionWindow > 0.48 && echoBox.breakout_risk < 0.36) {
    recommendation_label = '轻量叙事降压'
    recommendation_text = '当前 EchoBox 高热但外溢较弱，过度回应可能反而扩圈。'
  } else if ((thirdParty?.gravitational_pull || 0) > 0.34) {
    recommendation_label = '第三方解释辅助'
    recommendation_text = '第三方解释可帮助中立参与者理解事实链，但仍需保留来源复核。'
  } else if ((official?.gravitational_pull || 0) > 0.28) {
    recommendation_label = '澄清窗口可用'
    recommendation_text = '温和反对者存在中立化窗口，适合补充可核验事实说明。'
  }

  return {
    clarification_priority: clamp01((official?.gravitational_pull || 0) * 0.74 + campDynamics.neutralization_score * 0.3),
    faq_priority: clamp01((thirdParty?.gravitational_pull || 0) * 0.66 + neutralShare * 0.34),
    third_party_explanation_priority: clamp01(thirdParty?.gravitational_pull || 0),
    deconstruction_window_score: deconstructionWindow,
    wait_and_monitor_score: clamp01(0.56 - echoBox.breakout_risk * 0.42 + neutralShare * 0.12),
    recommendation_label,
    recommendation_text,
    risk_notes: [
      '当前使用前端本地 synthetic EvidenceItem fixture 映射。',
      '低信任或待复核证据只作为弱信号，不支撑高置信结论。',
    ],
    parameter_source: PARAMETER_SOURCE,
  }
}

export function buildReputationMemory(echoBoxes, peopleClusters, responseTempo) {
  const echoBox = echoBoxes[0]
  const dormant = peopleClusters.filter((cluster) => cluster.camp_state === 'dormant_grievance')
  const withdrawn = peopleClusters.filter((cluster) => cluster.camp_state === 'withdrawn')
  const unresolved = clamp01(dormant.length / Math.max(1, peopleClusters.length) * 0.58 + echoBox.breakout_risk * 0.36)
  return {
    unresolved_grievance_score: unresolved,
    stigma_persistence: clamp01(unresolved * 0.58 + echoBox.internal_reinforcement * 0.22),
    meme_persistence: clamp01(responseTempo.deconstruction_window_score * 0.36),
    trust_recovery: clamp01(0.62 - unresolved * 0.42 + responseTempo.clarification_priority * 0.18),
    reactivation_risk: clamp01(unresolved * 0.66 + withdrawn.length / Math.max(1, peopleClusters.length) * 0.2),
    monitoring_notes: ['退出讨论不等于问题解决；fixture mapping 不代表真实 case 数据。'],
    parameter_source: PARAMETER_SOURCE,
  }
}

export function normalizeMappedScenario(mapped) {
  const echoBox = mapped.echoBoxes[0]
  return {
    echoBox,
    influenceCores: mapped.influenceCores,
    peopleClusters: mapped.peopleClusters,
    campDynamics: mapped.campDynamics,
    deconstructionCore: mapped.deconstructionCores[0],
    responseTempo: mapped.responseTempo,
    reputationMemory: mapped.reputationMemory,
    sourceIdentities: mapped.sourceIdentities,
    evidenceRoles: mapped.evidenceRoles,
    evidenceSummary: mapped.evidenceSummary,
    mappingStatus: {
      mode: 'evidence_fixture_mapping',
      label: 'Evidence fixture mapping mode',
      notes: [
        '当前使用前端本地 synthetic EvidenceItem fixture 映射。',
        '不接 backend。',
        '不代表真实 case 数据。',
        '不代表全网全量覆盖。',
        '不代表因果确定。',
        '不执行真实平台动作。',
      ],
    },
  }
}

export function mapEvidenceToOpinionEcosystem(evidenceItems) {
  const evidenceRoles = evidenceItems.map(classifyEvidenceRole)
  const sourceIdentities = buildSourceIdentities(evidenceItems)
  const influenceCores = buildInfluenceCores(evidenceItems)
  const echoBoxes = buildEchoBoxes(evidenceItems, influenceCores)
  const peopleClusters = buildPeopleClusters(evidenceItems, echoBoxes)
  const campDynamics = buildCampDynamics(echoBoxes, influenceCores, peopleClusters)
  const deconstructionCores = buildDeconstructionCores(evidenceItems, influenceCores)
  const responseTempo = buildResponseTempo(echoBoxes, influenceCores, peopleClusters, campDynamics, deconstructionCores)
  const reputationMemory = buildReputationMemory(echoBoxes, peopleClusters, responseTempo)
  const rejectedCount = evidenceItems.filter((item) => item.review_status === 'rejected').length
  const duplicateGroupCount = new Set(evidenceItems.filter((item) => item.duplicate_group_id).map((item) => item.duplicate_group_id)).size
  const lowTrustCount = evidenceItems.filter((item) => ['low', 'unverified', 'medium_low'].includes(item.trust_label)).length

  return normalizeMappedScenario({
    sourceIdentities,
    evidenceRoles,
    influenceCores,
    echoBoxes,
    peopleClusters,
    campDynamics,
    deconstructionCores,
    responseTempo,
    reputationMemory,
    evidenceSummary: {
      total_evidence: evidenceItems.length,
      active_evidence: activeEvidence(evidenceItems).length,
      rejected_evidence: rejectedCount,
      duplicate_group_count: duplicateGroupCount,
      low_trust_or_unreviewed: lowTrustCount,
      parameter_source: PARAMETER_SOURCE,
    },
  })
}
