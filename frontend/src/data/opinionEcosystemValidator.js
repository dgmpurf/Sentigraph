const PASS = 'pass'
const WARN = 'warn'
const FAIL = 'fail'

const WEIGHT_KEY_PATTERN =
  /(score|ratio|rate|risk|capacity|reinforcement|confidence|credibility|weight|pull|power|potential|resistance|acceptance|intensity|strength|fatigue|memory|mobility|lock|sensitivity|cost|priority|recovery|persistence)$/i

const WEIGHT_KEY_EXCLUSIONS = new Set(['stance_score'])

function check(id, label, status, message, details = []) {
  return { id, label, status, message, details }
}

function isPlainObject(value) {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value)
}

function isWeightLikeKey(key) {
  return WEIGHT_KEY_PATTERN.test(key) && !WEIGHT_KEY_EXCLUSIONS.has(key)
}

function flattenEvidenceIdsFromClusters(peopleClusters = []) {
  return peopleClusters.flatMap((cluster) => cluster.evidence_ids || [])
}

function collectReferencedEvidenceIds(mappedScenario) {
  return new Set([
    ...flattenEvidenceIdsFromClusters(mappedScenario.peopleClusters),
    ...(mappedScenario.influenceCores || []).map((core) => core.source_evidence_id).filter(Boolean),
    ...((mappedScenario.influenceCores || []).flatMap((core) => core.evidence_ids || [])),
  ])
}

export function validateWeightRange(object, path = 'scenario') {
  const issues = []

  function visit(value, currentPath) {
    if (Array.isArray(value)) {
      value.forEach((item, index) => visit(item, `${currentPath}[${index}]`))
      return
    }
    if (!isPlainObject(value)) return

    Object.entries(value).forEach(([key, nestedValue]) => {
      const nextPath = `${currentPath}.${key}`
      if (typeof nestedValue === 'number' && isWeightLikeKey(key)) {
        if (!Number.isFinite(nestedValue) || nestedValue < 0 || nestedValue > 1) {
          issues.push(`${nextPath}=${nestedValue}`)
        }
      } else if (isPlainObject(nestedValue) || Array.isArray(nestedValue)) {
        visit(nestedValue, nextPath)
      }
    })
  }

  visit(object, path)
  return check(
    'weight_range',
    '权重范围',
    issues.length ? FAIL : PASS,
    issues.length ? `发现 ${issues.length} 个权重类字段不在 0-1 范围内。` : '所有权重类字段均在 0-1 范围内。',
    issues,
  )
}

export function validateNoRawIdentityLeak(peopleClusters = []) {
  const leakingClusters = peopleClusters
    .filter((cluster) => 'author_id' in cluster || 'author_name' in cluster || 'source_actor_hashes' in cluster)
    .map((cluster) => cluster.cluster_id)

  return check(
    'people_cluster_anonymized',
    '人群簇匿名化',
    leakingClusters.length ? FAIL : PASS,
    leakingClusters.length
      ? 'PeopleCluster 暴露了 raw author_id / author_name / actor hash 字段。'
      : 'PeopleCluster 仅展示人群簇与 evidence_ids，不暴露 raw author_id 或 raw author_name。',
    leakingClusters,
  )
}

export function validateEvidenceGating(evidenceItems = [], mappedScenario) {
  const rejectedIds = new Set(evidenceItems.filter((item) => item.review_status === 'rejected').map((item) => item.evidence_id))
  const referencedIds = collectReferencedEvidenceIds(mappedScenario)
  const leakedRejected = Array.from(rejectedIds).filter((id) => referencedIds.has(id))
  const expectedActive = evidenceItems.length - rejectedIds.size
  const activeSummary = mappedScenario.evidenceSummary?.active_evidence
  const summaryMatches = activeSummary === undefined || activeSummary === expectedActive

  if (leakedRejected.length) {
    return check(
      'rejected_evidence_gate',
      'rejected 证据门控',
      FAIL,
      '被驳回 evidence 仍出现在活跃映射对象引用中。',
      leakedRejected,
    )
  }

  if (!summaryMatches) {
    return check(
      'rejected_evidence_gate',
      'rejected 证据门控',
      WARN,
      '被驳回 evidence 未进入对象引用，但 summary active_evidence 与 fixture 数量不一致。',
      [`expected=${expectedActive}`, `actual=${activeSummary}`],
    )
  }

  return check(
    'rejected_evidence_gate',
    'rejected 证据门控',
    PASS,
    '被驳回 evidence 未进入 InfluenceCore / PeopleCluster 活跃权重引用。',
  )
}

export function validateDuplicateHandling(evidenceItems = [], mappedScenario) {
  const groupToIds = evidenceItems.reduce((acc, item) => {
    if (!item.duplicate_group_id) return acc
    if (!acc.has(item.duplicate_group_id)) acc.set(item.duplicate_group_id, [])
    acc.get(item.duplicate_group_id).push(item.evidence_id)
    return acc
  }, new Map())

  const clusterEvidenceIds = new Set(flattenEvidenceIdsFromClusters(mappedScenario.peopleClusters))
  const duplicatedReferences = []
  groupToIds.forEach((ids, groupId) => {
    const referencedCount = ids.filter((id) => clusterEvidenceIds.has(id)).length
    if (referencedCount > 1) duplicatedReferences.push(`${groupId}:${referencedCount}`)
  })

  if (duplicatedReferences.length) {
    return check(
      'duplicate_collapse',
      '重复证据折叠',
      FAIL,
      '同一 duplicate_group_id 内有多条 evidence 被当作独立人群表达引用。',
      duplicatedReferences,
    )
  }

  return check(
    'duplicate_collapse',
    '重复证据折叠',
    PASS,
    groupToIds.size
      ? '重复 evidence 已折叠，不会作为独立声音放大 PeopleCluster 数量。'
      : '当前 fixture 未发现 duplicate_group_id；折叠检查无冲突。',
  )
}

export function validateLowTrustHandling(evidenceItems = [], mappedScenario) {
  const lowTrustItems = evidenceItems.filter(
    (item) =>
      ['low', 'medium_low', 'unverified'].includes(item.trust_label) ||
      ['marked_weak', 'review_needed'].includes(item.review_status),
  )
  const hasRiskNote = (mappedScenario.responseTempo?.risk_notes || []).some((note) => String(note).includes('低信任') || String(note).includes('待复核'))
  const hasSummary = (mappedScenario.evidenceSummary?.low_trust_or_unreviewed || 0) >= lowTrustItems.length

  if (!lowTrustItems.length) {
    return check('low_trust_gate', '低信任 / 待复核降权', WARN, 'fixture 中没有低信任或待复核样本，无法验证降权提示。')
  }
  if (!hasRiskNote && !hasSummary) {
    return check(
      'low_trust_gate',
      '低信任 / 待复核降权',
      WARN,
      '存在低信任或待复核样本，但 UI summary / risk notes 未明确提示。',
    )
  }
  return check(
    'low_trust_gate',
    '低信任 / 待复核降权',
    PASS,
    '低信任、marked_weak、needs_review evidence 被统计或风险说明标记，不会主导高置信结论。',
  )
}

export function validateObjectSeparation(mappedScenario) {
  const clusterIds = new Set((mappedScenario.peopleClusters || []).map((cluster) => cluster.cluster_id))
  const coreIds = new Set((mappedScenario.influenceCores || []).map((core) => core.core_id))
  const overlap = Array.from(coreIds).filter((id) => clusterIds.has(id))
  const clustersWithCoreShape = (mappedScenario.peopleClusters || []).filter((cluster) => 'core_type' in cluster || 'gravitational_pull' in cluster)
  const hasDeconstructionCore = Boolean(mappedScenario.deconstructionCore?.core_id)

  if (overlap.length || clustersWithCoreShape.length || !hasDeconstructionCore) {
    return check(
      'object_separation',
      'InfluenceCore 与小球分离',
      FAIL,
      'InfluenceCore / DeconstructionCore 与 PeopleCluster 结构未保持清晰分离。',
      [...overlap, ...clustersWithCoreShape.map((cluster) => cluster.cluster_id), hasDeconstructionCore ? '' : 'missing_deconstruction_core'].filter(Boolean),
    )
  }

  return check(
    'object_separation',
    'InfluenceCore 与小球分离',
    PASS,
    'InfluenceCore 和 DeconstructionCore 独立于 PeopleCluster 小球渲染数据。',
  )
}

export function validateEchoBoxBoundary(mappedScenario) {
  const echoBox = mappedScenario.echoBox
  const requiredFields = ['saturation_ratio', 'permeability_score', 'breakout_risk', 'internal_reinforcement']
  const missingFields = requiredFields.filter((field) => typeof echoBox?.[field] !== 'number')
  const outOfRange = requiredFields.filter((field) => typeof echoBox?.[field] === 'number' && (echoBox[field] < 0 || echoBox[field] > 1))

  if (!echoBox || missingFields.length || outOfRange.length) {
    return check(
      'echo_box_boundary',
      'EchoBox 边界指标',
      FAIL,
      'EchoBox 缺少边界指标或指标不在 0-1 范围内。',
      [...missingFields.map((field) => `missing:${field}`), ...outOfRange.map((field) => `range:${field}`)],
    )
  }

  return check('echo_box_boundary', 'EchoBox 边界指标', PASS, 'EchoBox 包含 saturation / permeability / breakout / reinforcement 边界指标。')
}

export function validateResponseTempo(mappedScenario) {
  const responseTempo = mappedScenario.responseTempo
  const hasText = Boolean(responseTempo?.recommendation_text)
  const hasRiskNotes = Array.isArray(responseTempo?.risk_notes) && responseTempo.risk_notes.length > 0

  return check(
    'response_tempo_output',
    'ResponseTempo 输出',
    hasText && hasRiskNotes ? PASS : FAIL,
    hasText && hasRiskNotes ? 'ResponseTempo 包含建议文本和 risk notes。' : 'ResponseTempo 缺少建议文本或 risk notes。',
  )
}

export function validateReputationMemory(mappedScenario) {
  const memory = mappedScenario.reputationMemory
  const requiredFields = ['unresolved_grievance_score', 'reactivation_risk']
  const missingFields = requiredFields.filter((field) => typeof memory?.[field] !== 'number')

  return check(
    'reputation_memory_output',
    'ReputationMemory 输出',
    missingFields.length ? FAIL : PASS,
    missingFields.length ? 'ReputationMemory 缺少 unresolved grievance / reactivation 字段。' : 'ReputationMemory 包含未解决不满和再激活风险字段。',
    missingFields,
  )
}

export function validateSafetyCopyFlags(mappedScenario) {
  const notes = [
    ...(mappedScenario.mappingStatus?.notes || []),
    ...(mappedScenario.responseTempo?.risk_notes || []),
  ].join(' ')
  const requiredFlags = ['不代表真实 case 数据', '不代表全网全量覆盖', '不代表因果确定', '不执行真实平台动作']
  const missingFlags = requiredFlags.filter((flag) => !notes.includes(flag))

  return check(
    'safety_copy_flags',
    '安全边界文案',
    missingFlags.length ? WARN : PASS,
    missingFlags.length ? 'mapping status / risk notes 中缺少部分安全边界提示，页面仍需保留顶层安全文案。' : '映射对象携带核心安全边界提示。',
    missingFlags,
  )
}

export function validateOpinionEcosystemScenario(mappedScenario, evidenceItems = []) {
  const checks = [
    validateWeightRange(mappedScenario),
    validateEvidenceGating(evidenceItems, mappedScenario),
    validateDuplicateHandling(evidenceItems, mappedScenario),
    validateLowTrustHandling(evidenceItems, mappedScenario),
    validateNoRawIdentityLeak(mappedScenario.peopleClusters),
    validateObjectSeparation(mappedScenario),
    validateEchoBoxBoundary(mappedScenario),
    validateResponseTempo(mappedScenario),
    validateReputationMemory(mappedScenario),
    validateSafetyCopyFlags(mappedScenario),
  ]
  return summarizeValidationResults(checks)
}

export function summarizeValidationResults(checks) {
  const failures = checks.filter((item) => item.status === FAIL)
  const warnings = checks.filter((item) => item.status === WARN)
  return {
    status: failures.length ? FAIL : warnings.length ? WARN : PASS,
    checks,
    warnings,
    failures,
    pass_count: checks.filter((item) => item.status === PASS).length,
    warn_count: warnings.length,
    fail_count: failures.length,
  }
}
