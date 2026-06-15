const clamp01 = (value) => Math.max(0, Math.min(1, Number(value) || 0))

export const HELLDIVERS_SCENARIO_TO_PHASE_ID = {
  natural: 't1',
  official_clarification: 't2',
  faq_explainer: 't3',
  third_party_explanation: 't3',
  community_deconstruction: 't4',
  delayed_response: 't5',
  no_response: 't1',
}

export const HELLDIVERS_PHASE_TO_SCENARIO_KEY = {
  t0: 'natural',
  t1: 'natural',
  t2: 'official_clarification',
  t3: 'third_party_explanation',
  t4: 'community_deconstruction',
  t5: 'delayed_response',
  t6: 'no_response',
}

export const HELLDIVERS_TIMELINE_PRESETS = [
  {
    phase_id: 't0',
    label_zh: 'T0 账号绑定公告',
    label_en: 'Account linking announcement',
    short_explanation_zh: '官方更新成为事件触发点，讨论边界开始收缩，玩家开始核对规则、地区可用性和账号要求。',
    related_influence_core_ids: ['official_statement', 'community_backlash'],
    echo_box_effects: {
      saturation: 0.55,
      permeability: 0.38,
      breakout_risk: 0.3,
      reinforcement: 0.46,
    },
    camp_effects: {
      support: 0.12,
      neutral: 0.33,
      oppose: 0.36,
      swing: 0.11,
      withdrawn: 0.02,
      dormant_grievance: 0.06,
    },
    v2_metrics: {
      neutralization_trend: 0.16,
      withdrawal_fatigue: 0.08,
      backlash_risk: 0.24,
      breakout_risk: 0.3,
      deconstruction_window: 0.08,
      dormant_grievance_risk: 0.22,
    },
    visual_effects: {
      official_core_strength: 0.36,
      backlash_core_strength: 0.42,
      explanation_core_strength: 0.12,
      deconstruction_core_strength: 0.04,
      bridge_cluster_strength: 0.12,
      red_cluster_glow: 0.18,
      neutral_cluster_density: 0.18,
      withdrawn_opacity: 0.08,
      boundary_pulse: 0.2,
    },
    response_tempo_note_zh: '先确认事实边界：规则是什么、哪些地区受影响、下一次更新时间是什么。',
    public_copy_zh: '这一步展示公告触发后的讨论聚焦，不代表完整历史重建。',
  },
  {
    phase_id: 't1',
    label_zh: 'T1 社区反弹',
    label_en: 'Community backlash',
    short_explanation_zh: '地区可用性、购买后规则变化和信任预期成为主要表达点，EchoBox 饱和度与破圈风险升高。',
    related_influence_core_ids: ['community_backlash'],
    echo_box_effects: {
      saturation: 0.82,
      permeability: 0.18,
      breakout_risk: 0.64,
      reinforcement: 0.72,
    },
    camp_effects: {
      support: 0.06,
      neutral: 0.2,
      oppose: 0.58,
      swing: 0.08,
      withdrawn: 0.01,
      dormant_grievance: 0.07,
    },
    v2_metrics: {
      neutralization_trend: 0.06,
      withdrawal_fatigue: 0.08,
      backlash_risk: 0.58,
      breakout_risk: 0.64,
      deconstruction_window: 0.05,
      dormant_grievance_risk: 0.38,
    },
    visual_effects: {
      official_core_strength: 0.08,
      backlash_core_strength: 0.72,
      explanation_core_strength: 0.08,
      deconstruction_core_strength: 0.04,
      bridge_cluster_strength: 0.08,
      red_cluster_glow: 0.56,
      neutral_cluster_density: 0.06,
      withdrawn_opacity: 0.04,
      boundary_pulse: 0.72,
    },
    response_tempo_note_zh: '不要把低响应误读成问题消失；此阶段需要清晰、可核验、低姿态的事实说明。',
    public_copy_zh: '这一步展示公开样本中的社区反弹聚焦，不代表全平台玩家分布。',
  },
  {
    phase_id: 't2',
    label_zh: 'T2 官方撤回',
    label_en: 'Rollback / update not moving forward',
    short_explanation_zh: '官方更新降低短期冲突强度，官方核心增强，反弹光晕降温，但声誉记忆不会立刻清零。',
    related_influence_core_ids: ['official_statement', 'community_backlash'],
    echo_box_effects: {
      saturation: 0.5,
      permeability: 0.52,
      breakout_risk: 0.24,
      reinforcement: 0.32,
    },
    camp_effects: {
      support: 0.18,
      neutral: 0.42,
      oppose: 0.24,
      swing: 0.09,
      withdrawn: 0.04,
      dormant_grievance: 0.03,
    },
    v2_metrics: {
      neutralization_trend: 0.46,
      withdrawal_fatigue: 0.16,
      backlash_risk: 0.14,
      breakout_risk: 0.24,
      deconstruction_window: 0.14,
      dormant_grievance_risk: 0.2,
    },
    visual_effects: {
      official_core_strength: 0.72,
      backlash_core_strength: 0.24,
      explanation_core_strength: 0.18,
      deconstruction_core_strength: 0.08,
      bridge_cluster_strength: 0.18,
      red_cluster_glow: 0.08,
      neutral_cluster_density: 0.44,
      withdrawn_opacity: 0.12,
      boundary_pulse: 0.12,
    },
    response_tempo_note_zh: '撤回或更新能先降压，但仍要解释地区可用性、既有购买者预期和后续安排。',
    public_copy_zh: '这一步展示撤回后的短期降压效果，不代表信任已经完全恢复。',
  },
  {
    phase_id: 't3',
    label_zh: 'T3 媒体解释',
    label_en: 'Third-party media explanation',
    short_explanation_zh: '第三方整理帮助中立与观望人群理解时间线和争议核心，桥接簇变得更明显。',
    related_influence_core_ids: ['media_explanation', 'official_statement'],
    echo_box_effects: {
      saturation: 0.44,
      permeability: 0.58,
      breakout_risk: 0.2,
      reinforcement: 0.3,
    },
    camp_effects: {
      support: 0.14,
      neutral: 0.48,
      oppose: 0.2,
      swing: 0.11,
      withdrawn: 0.04,
      dormant_grievance: 0.03,
    },
    v2_metrics: {
      neutralization_trend: 0.42,
      withdrawal_fatigue: 0.16,
      backlash_risk: 0.12,
      breakout_risk: 0.2,
      deconstruction_window: 0.28,
      dormant_grievance_risk: 0.16,
    },
    visual_effects: {
      official_core_strength: 0.24,
      backlash_core_strength: 0.2,
      explanation_core_strength: 0.72,
      deconstruction_core_strength: 0.16,
      bridge_cluster_strength: 0.52,
      red_cluster_glow: 0.08,
      neutral_cluster_density: 0.48,
      withdrawn_opacity: 0.1,
      boundary_pulse: 0.08,
    },
    response_tempo_note_zh: 'FAQ 或第三方说明适合承接事实争议，但仍需要保留来源与人工复核说明。',
    public_copy_zh: '这一步展示解释型内容对中立化的辅助作用，不代表第三方内容就是官方验证。',
  },
  {
    phase_id: 't4',
    label_zh: 'T4 社区解构',
    label_en: 'Review Bomb Cape / deconstruction',
    short_explanation_zh: 'Review Bomb Cape 等社区符号把高热冲突转成可讨论的梗与记忆，解构核心增强，部分热簇降温。',
    related_influence_core_ids: ['deconstruction_meme', 'community_backlash'],
    echo_box_effects: {
      saturation: 0.42,
      permeability: 0.62,
      breakout_risk: 0.16,
      reinforcement: 0.26,
    },
    camp_effects: {
      support: 0.16,
      neutral: 0.36,
      oppose: 0.16,
      swing: 0.13,
      withdrawn: 0.14,
      dormant_grievance: 0.05,
    },
    v2_metrics: {
      neutralization_trend: 0.5,
      withdrawal_fatigue: 0.3,
      backlash_risk: 0.1,
      breakout_risk: 0.16,
      deconstruction_window: 0.66,
      dormant_grievance_risk: 0.18,
    },
    visual_effects: {
      official_core_strength: 0.16,
      backlash_core_strength: 0.18,
      explanation_core_strength: 0.28,
      deconstruction_core_strength: 0.78,
      bridge_cluster_strength: 0.44,
      red_cluster_glow: 0.06,
      neutral_cluster_density: 0.38,
      withdrawn_opacity: 0.24,
      boundary_pulse: 0.02,
    },
    response_tempo_note_zh: '社区解构可以降压，但要避免把梗误读成问题已经彻底解决。',
    public_copy_zh: '这一步展示社区符号如何沉淀为记忆，不代表平台采取了真实行动。',
  },
  {
    phase_id: 't5',
    label_zh: 'T5 疲劳衰减',
    label_en: 'Fatigue and cooling',
    short_explanation_zh: '讨论强度下降，退出与疲劳增加，但潜伏不满仍可能在后续事件中被再激活。',
    related_influence_core_ids: ['deconstruction_meme', 'media_explanation'],
    echo_box_effects: {
      saturation: 0.36,
      permeability: 0.54,
      breakout_risk: 0.2,
      reinforcement: 0.22,
    },
    camp_effects: {
      support: 0.12,
      neutral: 0.28,
      oppose: 0.14,
      swing: 0.08,
      withdrawn: 0.28,
      dormant_grievance: 0.1,
    },
    v2_metrics: {
      neutralization_trend: 0.34,
      withdrawal_fatigue: 0.56,
      backlash_risk: 0.18,
      breakout_risk: 0.2,
      deconstruction_window: 0.34,
      dormant_grievance_risk: 0.32,
    },
    visual_effects: {
      official_core_strength: 0.14,
      backlash_core_strength: 0.26,
      explanation_core_strength: 0.22,
      deconstruction_core_strength: 0.34,
      bridge_cluster_strength: 0.22,
      red_cluster_glow: 0.16,
      neutral_cluster_density: 0.18,
      withdrawn_opacity: 0.42,
      boundary_pulse: 0.22,
    },
    response_tempo_note_zh: '热度下降不是自动恢复；需要监测后续相似政策、地区可用性或账号要求是否再触发。',
    public_copy_zh: '这一步展示疲劳和退出，不代表争议已经从声誉记忆中消失。',
  },
  {
    phase_id: 't6',
    label_zh: 'T6 声誉记忆',
    label_en: 'Reputation memory',
    short_explanation_zh: '事件沉淀为长期记忆符号，后续相关更新可能重新激活信任讨论和区域可用性担忧。',
    related_influence_core_ids: ['deconstruction_meme', 'community_backlash'],
    echo_box_effects: {
      saturation: 0.46,
      permeability: 0.42,
      breakout_risk: 0.34,
      reinforcement: 0.38,
    },
    camp_effects: {
      support: 0.1,
      neutral: 0.3,
      oppose: 0.2,
      swing: 0.08,
      withdrawn: 0.16,
      dormant_grievance: 0.16,
    },
    v2_metrics: {
      neutralization_trend: 0.22,
      withdrawal_fatigue: 0.34,
      backlash_risk: 0.28,
      breakout_risk: 0.34,
      deconstruction_window: 0.28,
      dormant_grievance_risk: 0.52,
    },
    visual_effects: {
      official_core_strength: 0.12,
      backlash_core_strength: 0.38,
      explanation_core_strength: 0.18,
      deconstruction_core_strength: 0.44,
      bridge_cluster_strength: 0.18,
      red_cluster_glow: 0.28,
      neutral_cluster_density: 0.18,
      withdrawn_opacity: 0.26,
      boundary_pulse: 0.42,
    },
    response_tempo_note_zh: '声誉记忆阶段适合持续透明沟通与复盘，不适合把沉默视为完全恢复。',
    public_copy_zh: '这一步展示长期记忆和再激活风险，不代表可预测真实未来。',
  },
]

export function getHelldiversTimelinePreset(phaseId) {
  return HELLDIVERS_TIMELINE_PRESETS.find((preset) => preset.phase_id === phaseId) || HELLDIVERS_TIMELINE_PRESETS[0]
}

export function applyHelldiversTimelinePresetToScenario(scenario, phaseId) {
  const preset = getHelldiversTimelinePreset(phaseId)
  const next = JSON.parse(JSON.stringify(scenario))
  const coreBoostByRole = {
    official: preset.visual_effects.official_core_strength,
    opposition: preset.visual_effects.backlash_core_strength,
    third_party: preset.visual_effects.explanation_core_strength,
    deconstruction: preset.visual_effects.deconstruction_core_strength,
    neutral_analysis: preset.visual_effects.explanation_core_strength * 0.58,
  }

  next.helldiversTimelinePreset = preset
  next.timelinePhaseId = preset.phase_id
  next.timelinePhaseLabel = `${preset.label_zh} / ${preset.label_en}`

  next.echoBox.echo_chamber_score = clamp01(preset.echo_box_effects.reinforcement)
  next.echoBox.saturation_ratio = clamp01(preset.echo_box_effects.saturation)
  next.echoBox.permeability_score = clamp01(preset.echo_box_effects.permeability)
  next.echoBox.breakout_risk = clamp01(preset.echo_box_effects.breakout_risk)
  next.echoBox.internal_reinforcement = clamp01(preset.echo_box_effects.reinforcement)
  next.echoBox.fatigue_rate = clamp01(preset.v2_metrics.withdrawal_fatigue * 0.6)

  next.campDynamics.neutralization_score = clamp01(preset.v2_metrics.neutralization_trend)
  next.campDynamics.withdrawal_score = clamp01(preset.v2_metrics.withdrawal_fatigue)
  next.campDynamics.backlash_score = clamp01(preset.v2_metrics.backlash_risk)
  next.campDynamics.hardening_score = clamp01(preset.echo_box_effects.reinforcement * 0.54)
  next.campDynamics.conversion_score = clamp01(preset.camp_effects.swing + preset.camp_effects.neutral * 0.32)
  next.campDynamics.reactivation_risk = clamp01(preset.v2_metrics.dormant_grievance_risk)

  next.responseTempo.deconstruction_window_score = clamp01(preset.v2_metrics.deconstruction_window)
  next.responseTempo.clarification_priority = clamp01(coreBoostByRole.official)
  next.responseTempo.faq_priority = clamp01(coreBoostByRole.third_party)
  next.responseTempo.third_party_explanation_priority = clamp01(coreBoostByRole.third_party)
  next.responseTempo.wait_and_monitor_score = clamp01(0.5 - preset.v2_metrics.breakout_risk * 0.28 + preset.v2_metrics.withdrawal_fatigue * 0.2)
  next.responseTempo.recommendation_label = preset.label_zh
  next.responseTempo.recommendation_text = preset.response_tempo_note_zh
  next.responseTempo.risk_notes = [preset.public_copy_zh, 'local timeline preset only; not full-web coverage, not official verification, not causal proof.']

  next.reputationMemory.unresolved_grievance_score = clamp01(preset.v2_metrics.dormant_grievance_risk)
  next.reputationMemory.reactivation_risk = clamp01(preset.v2_metrics.dormant_grievance_risk)
  next.reputationMemory.stigma_persistence = clamp01(preset.v2_metrics.dormant_grievance_risk * 0.72 + preset.v2_metrics.backlash_risk * 0.2)
  next.reputationMemory.meme_persistence = clamp01(preset.v2_metrics.deconstruction_window * 0.52)
  next.reputationMemory.trust_recovery = clamp01(0.58 + preset.v2_metrics.neutralization_trend * 0.28 - preset.v2_metrics.dormant_grievance_risk * 0.34)

  next.influenceCores = next.influenceCores.map((core) => {
    const roleKey = core.core_id || 'third_party'
    const boost = coreBoostByRole[roleKey] ?? 0.18
    return {
      ...core,
      gravitational_pull: clamp01(boost),
      bridge_power: clamp01((core.bridge_power || 0) * 0.52 + preset.visual_effects.bridge_cluster_strength * 0.48),
      breakout_power: clamp01(roleKey === 'opposition' ? preset.v2_metrics.breakout_risk : (core.breakout_power || 0) * 0.5),
      neutral_acceptance: clamp01((core.neutral_acceptance || 0) * 0.5 + preset.v2_metrics.neutralization_trend * 0.5),
      backlash_risk: clamp01(roleKey === 'opposition' ? preset.v2_metrics.backlash_risk : (core.backlash_risk || 0) * 0.55),
    }
  })

  return next
}
