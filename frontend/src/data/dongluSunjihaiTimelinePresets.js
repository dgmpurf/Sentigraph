const clamp01 = (value) => Math.max(0, Math.min(1, Number(value) || 0))

export const DONGLU_SUNJIHAI_SCENARIO_TO_PHASE_ID = {
  natural: 't1',
  official_clarification: 't2',
  faq_explainer: 't3',
  third_party_explanation: 't3',
  community_deconstruction: 't4',
  delayed_response: 't5',
  no_response: 't6',
}

export const DONGLU_SUNJIHAI_PHASE_TO_SCENARIO_KEY = {
  t0: 'natural',
  t1: 'natural',
  t2: 'official_clarification',
  t3: 'third_party_explanation',
  t4: 'community_deconstruction',
  t5: 'delayed_response',
  t6: 'no_response',
}

export const DONGLU_SUNJIHAI_TIMELINE_PRESETS = [
  {
    phase_id: 't0',
    label_zh: 'T0 争议背景进入公众视野',
    label_en: 'Background enters public view',
    short_explanation_zh:
      '围绕中国足球青训路线分歧的公开讨论进入样本视野。此阶段只表示本地受控样本中的背景进入点，不是完整历史重建。',
    scenario_keys: ['natural'],
    related_influence_core_ids: ['neutral_analysis', 'third_party'],
    echo_box_effects: {
      saturation: 0.42,
      permeability: 0.46,
      breakout_risk: 0.24,
      reinforcement: 0.34,
    },
    camp_effects: {
      support: 0.18,
      neutral: 0.42,
      oppose: 0.22,
      swing: 0.12,
      withdrawn: 0.03,
      dormant_grievance: 0.03,
    },
    v2_metrics: {
      neutralization_trend: 0.22,
      withdrawal_fatigue: 0.1,
      backlash_risk: 0.18,
      breakout_risk: 0.24,
      deconstruction_window: 0.12,
      dormant_grievance_risk: 0.2,
    },
    visual_effects: {
      official_core_strength: 0.12,
      backlash_core_strength: 0.22,
      explanation_core_strength: 0.34,
      deconstruction_core_strength: 0.1,
      bridge_cluster_strength: 0.18,
      red_cluster_glow: 0.12,
      neutral_cluster_density: 0.28,
      withdrawn_opacity: 0.06,
      boundary_pulse: 0.14,
    },
    response_tempo_note_zh:
      '先建立事实和样本边界：这只是本地历史复盘 preset，不代表完整历史重建、官方验证或因果证明。',
    public_copy_zh:
      'T0 展示争议背景进入公众视野后的初始讨论空间；它不是未来预测，也不是全网全量证据。',
  },
  {
    phase_id: 't1',
    label_zh: 'T1 社区讨论扩散',
    label_en: 'Community discussion spreads',
    short_explanation_zh:
      '微博、B 站、贴吧、虎扑、懂球帝等样本来源开始形成可观察的讨论簇。PeopleCluster 仍是匿名群体簇，不是真实个人。',
    scenario_keys: ['natural', 'delayed_response'],
    related_influence_core_ids: ['opposition', 'neutral_analysis'],
    echo_box_effects: {
      saturation: 0.66,
      permeability: 0.35,
      breakout_risk: 0.42,
      reinforcement: 0.52,
    },
    camp_effects: {
      support: 0.25,
      neutral: 0.28,
      oppose: 0.34,
      swing: 0.08,
      withdrawn: 0.02,
      dormant_grievance: 0.03,
    },
    v2_metrics: {
      neutralization_trend: 0.18,
      withdrawal_fatigue: 0.12,
      backlash_risk: 0.36,
      breakout_risk: 0.42,
      deconstruction_window: 0.12,
      dormant_grievance_risk: 0.28,
    },
    visual_effects: {
      official_core_strength: 0.08,
      backlash_core_strength: 0.5,
      explanation_core_strength: 0.22,
      deconstruction_core_strength: 0.1,
      bridge_cluster_strength: 0.14,
      red_cluster_glow: 0.34,
      neutral_cluster_density: 0.16,
      withdrawn_opacity: 0.06,
      boundary_pulse: 0.4,
    },
    response_tempo_note_zh:
      '此阶段适合补充来源边界和讨论方向说明，避免把样本讨论误读成全平台真实比例。',
    public_copy_zh:
      'T1 展示样本中社区讨论扩散；它不表示全网覆盖，也不判断谁对谁错。',
  },
  {
    phase_id: 't2',
    label_zh: 'T2 阵营化与青训路线分歧',
    label_en: 'Camp split around youth-training routes',
    short_explanation_zh:
      '讨论从单点争议转向青训模式、项目责任、中国足球可信度和公共表达边界。这里展示的是样本中的讨论方向，不是事实结论。',
    scenario_keys: ['official_clarification', 'faq_explainer'],
    related_influence_core_ids: ['opposition', 'neutral_analysis'],
    echo_box_effects: {
      saturation: 0.72,
      permeability: 0.28,
      breakout_risk: 0.48,
      reinforcement: 0.58,
    },
    camp_effects: {
      support: 0.3,
      neutral: 0.22,
      oppose: 0.36,
      swing: 0.06,
      withdrawn: 0.03,
      dormant_grievance: 0.03,
    },
    v2_metrics: {
      neutralization_trend: 0.12,
      withdrawal_fatigue: 0.16,
      backlash_risk: 0.42,
      breakout_risk: 0.48,
      deconstruction_window: 0.18,
      dormant_grievance_risk: 0.34,
    },
    visual_effects: {
      official_core_strength: 0.12,
      backlash_core_strength: 0.62,
      explanation_core_strength: 0.26,
      deconstruction_core_strength: 0.14,
      bridge_cluster_strength: 0.1,
      red_cluster_glow: 0.44,
      neutral_cluster_density: 0.12,
      withdrawn_opacity: 0.1,
      boundary_pulse: 0.5,
    },
    response_tempo_note_zh:
      '如果需要解释，应以透明沟通、证据边界和青训制度背景为主，不应进行个体定向或隐性操控。',
    public_copy_zh:
      'T2 展示青训路线分歧在样本中的阵营化倾向；这不是官方确认或全网证明。',
  },
  {
    phase_id: 't3',
    label_zh: 'T3 媒体转述与二次解释',
    label_en: 'Media reframing and secondary explanation',
    short_explanation_zh:
      '媒体、创作者视频和社区解释内容开始重述争议。InfluenceCore 表示内容/叙事/媒体核心，不是人群小球。',
    scenario_keys: ['third_party_explanation', 'faq_explainer'],
    related_influence_core_ids: ['third_party', 'neutral_analysis'],
    echo_box_effects: {
      saturation: 0.58,
      permeability: 0.48,
      breakout_risk: 0.28,
      reinforcement: 0.38,
    },
    camp_effects: {
      support: 0.22,
      neutral: 0.42,
      oppose: 0.22,
      swing: 0.08,
      withdrawn: 0.04,
      dormant_grievance: 0.02,
    },
    v2_metrics: {
      neutralization_trend: 0.36,
      withdrawal_fatigue: 0.18,
      backlash_risk: 0.22,
      breakout_risk: 0.28,
      deconstruction_window: 0.32,
      dormant_grievance_risk: 0.24,
    },
    visual_effects: {
      official_core_strength: 0.1,
      backlash_core_strength: 0.28,
      explanation_core_strength: 0.66,
      deconstruction_core_strength: 0.18,
      bridge_cluster_strength: 0.46,
      red_cluster_glow: 0.14,
      neutral_cluster_density: 0.42,
      withdrawn_opacity: 0.12,
      boundary_pulse: 0.18,
    },
    response_tempo_note_zh:
      '第三方说明可辅助中立化，但仍需要清楚标注来源、样本限制和人工复核状态。',
    public_copy_zh:
      'T3 展示媒体转述和二次解释的桥接作用；它不是官方验证，也不是事实裁定。',
  },
  {
    phase_id: 't4',
    label_zh: 'T4 情绪高峰与极端表达隔离',
    label_en: 'Emotional peak and isolated extreme expression',
    short_explanation_zh:
      '样本中可能出现更强烈的攻击或调侃表达，但这类极端表达簇可能自我隔离，降低桥接能力。这里描述聚合行为，不指认个人。',
    scenario_keys: ['community_deconstruction'],
    related_influence_core_ids: ['deconstruction', 'opposition'],
    echo_box_effects: {
      saturation: 0.76,
      permeability: 0.22,
      breakout_risk: 0.54,
      reinforcement: 0.64,
    },
    camp_effects: {
      support: 0.26,
      neutral: 0.16,
      oppose: 0.42,
      swing: 0.04,
      withdrawn: 0.08,
      dormant_grievance: 0.04,
    },
    v2_metrics: {
      neutralization_trend: 0.08,
      withdrawal_fatigue: 0.3,
      backlash_risk: 0.5,
      breakout_risk: 0.54,
      deconstruction_window: 0.42,
      dormant_grievance_risk: 0.38,
    },
    visual_effects: {
      official_core_strength: 0.06,
      backlash_core_strength: 0.7,
      explanation_core_strength: 0.18,
      deconstruction_core_strength: 0.58,
      bridge_cluster_strength: 0.08,
      red_cluster_glow: 0.58,
      neutral_cluster_density: 0.08,
      withdrawn_opacity: 0.24,
      boundary_pulse: 0.62,
    },
    response_tempo_note_zh:
      '极端表达簇需要被视为聚合讨论行为；不应引导其极端化，不应进行个体指认或定向影响。',
    public_copy_zh:
      'T4 展示样本内高情绪表达和极端表达隔离风险；这不是对个人或群体的定罪。',
  },
  {
    phase_id: 't5',
    label_zh: 'T5 舆论疲劳与普通用户退出',
    label_en: 'Fatigue and casual-user withdrawal',
    short_explanation_zh:
      '部分中立或普通用户可能疲劳退出，讨论空间收缩。退出讨论不等于问题解决，也不等于信任恢复。',
    scenario_keys: ['delayed_response'],
    related_influence_core_ids: ['neutral_analysis', 'deconstruction'],
    echo_box_effects: {
      saturation: 0.46,
      permeability: 0.38,
      breakout_risk: 0.3,
      reinforcement: 0.32,
    },
    camp_effects: {
      support: 0.16,
      neutral: 0.28,
      oppose: 0.22,
      swing: 0.04,
      withdrawn: 0.24,
      dormant_grievance: 0.06,
    },
    v2_metrics: {
      neutralization_trend: 0.24,
      withdrawal_fatigue: 0.58,
      backlash_risk: 0.22,
      breakout_risk: 0.3,
      deconstruction_window: 0.3,
      dormant_grievance_risk: 0.36,
    },
    visual_effects: {
      official_core_strength: 0.08,
      backlash_core_strength: 0.28,
      explanation_core_strength: 0.26,
      deconstruction_core_strength: 0.34,
      bridge_cluster_strength: 0.16,
      red_cluster_glow: 0.16,
      neutral_cluster_density: 0.2,
      withdrawn_opacity: 0.48,
      boundary_pulse: 0.28,
    },
    response_tempo_note_zh:
      '疲劳阶段适合复盘证据和边界，避免把沉默误读成共识或完整降温。',
    public_copy_zh:
      'T5 展示普通用户退出和舆论疲劳；它不是未来趋势预测。',
  },
  {
    phase_id: 't6',
    label_zh: 'T6 声誉记忆与长期议题沉淀',
    label_en: 'Reputation memory and long-term issue sediment',
    short_explanation_zh:
      '争议可能沉淀到更广泛的中国足球信任和青训声誉记忆中。此处只表示样本内可解释的长期议题痕迹。',
    scenario_keys: ['no_response'],
    related_influence_core_ids: ['deconstruction', 'third_party'],
    echo_box_effects: {
      saturation: 0.5,
      permeability: 0.34,
      breakout_risk: 0.38,
      reinforcement: 0.42,
    },
    camp_effects: {
      support: 0.14,
      neutral: 0.3,
      oppose: 0.24,
      swing: 0.04,
      withdrawn: 0.14,
      dormant_grievance: 0.14,
    },
    v2_metrics: {
      neutralization_trend: 0.18,
      withdrawal_fatigue: 0.36,
      backlash_risk: 0.3,
      breakout_risk: 0.38,
      deconstruction_window: 0.24,
      dormant_grievance_risk: 0.56,
    },
    visual_effects: {
      official_core_strength: 0.06,
      backlash_core_strength: 0.42,
      explanation_core_strength: 0.24,
      deconstruction_core_strength: 0.5,
      bridge_cluster_strength: 0.16,
      red_cluster_glow: 0.3,
      neutral_cluster_density: 0.18,
      withdrawn_opacity: 0.3,
      boundary_pulse: 0.44,
    },
    response_tempo_note_zh:
      '长期声誉记忆需要持续透明沟通与来源复核；不能把本地复盘解释成真实未来预测。',
    public_copy_zh:
      'T6 展示样本中的长期议题沉淀和再激活风险；它不是因果证明或官方结论。',
  },
]

export function getDongluSunjihaiTimelinePreset(phaseId) {
  return DONGLU_SUNJIHAI_TIMELINE_PRESETS.find((preset) => preset.phase_id === phaseId) || DONGLU_SUNJIHAI_TIMELINE_PRESETS[0]
}

export function applyDongluSunjihaiTimelinePresetToScenario(scenario, phaseId) {
  const preset = getDongluSunjihaiTimelinePreset(phaseId)
  const next = JSON.parse(JSON.stringify(scenario))
  const coreBoostByRole = {
    official: preset.visual_effects.official_core_strength,
    opposition: preset.visual_effects.backlash_core_strength,
    third_party: preset.visual_effects.explanation_core_strength,
    deconstruction: preset.visual_effects.deconstruction_core_strength,
    neutral_analysis: preset.visual_effects.explanation_core_strength * 0.72,
  }

  next.dongluSunjihaiTimelinePreset = preset
  next.historicalTimelinePreset = preset
  next.timelinePhaseId = preset.phase_id
  next.timelinePhaseLabel = `${preset.label_zh} / ${preset.label_en}`

  next.echoBox.echo_chamber_score = clamp01(preset.echo_box_effects.reinforcement)
  next.echoBox.saturation_ratio = clamp01(preset.echo_box_effects.saturation)
  next.echoBox.permeability_score = clamp01(preset.echo_box_effects.permeability)
  next.echoBox.breakout_risk = clamp01(preset.echo_box_effects.breakout_risk)
  next.echoBox.internal_reinforcement = clamp01(preset.echo_box_effects.reinforcement)
  next.echoBox.fatigue_rate = clamp01(preset.v2_metrics.withdrawal_fatigue * 0.62)

  next.campDynamics.neutralization_score = clamp01(preset.v2_metrics.neutralization_trend)
  next.campDynamics.withdrawal_score = clamp01(preset.v2_metrics.withdrawal_fatigue)
  next.campDynamics.backlash_score = clamp01(preset.v2_metrics.backlash_risk)
  next.campDynamics.hardening_score = clamp01(preset.echo_box_effects.reinforcement * 0.56)
  next.campDynamics.conversion_score = clamp01(preset.camp_effects.swing + preset.camp_effects.neutral * 0.26)
  next.campDynamics.reactivation_risk = clamp01(preset.v2_metrics.dormant_grievance_risk)

  next.responseTempo.deconstruction_window_score = clamp01(preset.v2_metrics.deconstruction_window)
  next.responseTempo.clarification_priority = clamp01(coreBoostByRole.official)
  next.responseTempo.faq_priority = clamp01(coreBoostByRole.third_party)
  next.responseTempo.third_party_explanation_priority = clamp01(coreBoostByRole.third_party)
  next.responseTempo.wait_and_monitor_score = clamp01(0.52 - preset.v2_metrics.breakout_risk * 0.24 + preset.v2_metrics.withdrawal_fatigue * 0.22)
  next.responseTempo.recommendation_label = preset.label_zh
  next.responseTempo.recommendation_text = preset.response_tempo_note_zh
  next.responseTempo.risk_notes = [
    preset.public_copy_zh,
    'local historical replay preset only; not prediction, not full reconstruction, not official verification, not causal proof.',
  ]

  next.reputationMemory.unresolved_grievance_score = clamp01(preset.v2_metrics.dormant_grievance_risk)
  next.reputationMemory.reactivation_risk = clamp01(preset.v2_metrics.dormant_grievance_risk)
  next.reputationMemory.stigma_persistence = clamp01(preset.v2_metrics.dormant_grievance_risk * 0.7 + preset.v2_metrics.backlash_risk * 0.18)
  next.reputationMemory.meme_persistence = clamp01(preset.v2_metrics.deconstruction_window * 0.45)
  next.reputationMemory.trust_recovery = clamp01(0.52 + preset.v2_metrics.neutralization_trend * 0.24 - preset.v2_metrics.dormant_grievance_risk * 0.3)

  next.influenceCores = next.influenceCores.map((core) => {
    const roleKey = core.core_id || 'third_party'
    const boost = coreBoostByRole[roleKey] ?? 0.18
    return {
      ...core,
      gravitational_pull: clamp01(boost),
      bridge_power: clamp01((core.bridge_power || 0) * 0.5 + preset.visual_effects.bridge_cluster_strength * 0.5),
      breakout_power: clamp01(roleKey === 'opposition' ? preset.v2_metrics.breakout_risk : (core.breakout_power || 0) * 0.45),
      neutral_acceptance: clamp01((core.neutral_acceptance || 0) * 0.52 + preset.v2_metrics.neutralization_trend * 0.48),
      backlash_risk: clamp01(roleKey === 'opposition' ? preset.v2_metrics.backlash_risk : (core.backlash_risk || 0) * 0.5),
    }
  })

  return next
}
