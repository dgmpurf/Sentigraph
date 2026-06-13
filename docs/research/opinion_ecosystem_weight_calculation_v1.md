# Sentigraph Opinion Ecosystem Weight Calculation v1

**更新时间**：2026-06-13  
**用途**：把 Sentigraph 的舆论生态模型转成第一版可解释权重体系，供后续文档、mock schema、小球沙盒视觉原型和 B 端报告设计使用。  
**性质**：这是研究 / 设计文档，不代表当前代码已经实现这些权重。当前 Sentigraph 仍保持 mock-default、YouTube-real-capable、Evidence-ingestion-ready、demo-ready 的边界。

---

## 0. 当前边界

本文件不改变当前项目边界：

```text
Sentigraph 不是全网自动爬虫。
当前真实官方 API 路径只有可选 YouTube。
CSV/Excel、Manual URL、Search Discovery、Vendor POC 是 Evidence 入口。
Search Discovery / RSS / GDELT 当前是 mock/static，不是 live provider。
供应商数据默认 vendor_attested / medium_low，不是官方验证。
MediaCrawler 不集成主线。
OpenClaw / 龙虾只能作为外部人工辅助工具。
抖音 / B站 / 小红书 / Reddit / 微博等真实接入仍 pending。
LLM 仍是 mock。
Evidence Scale / Coverage 不代表全网全量覆盖。
```

本文件新增的是 Evidence 之上的模型权重层：

```text
EvidenceItem
→ Influence Core / Narrative Core
→ EchoBox
→ People Cluster
→ Camp Dynamics
→ Deconstruction Core
→ Case Lifecycle
→ Response Tempo
→ Reputation Memory
```

---

## 1. 总原则

### 1.1 所有权重先统一成 0–1

内部计算使用：

```text
0.0 – 1.0
```

UI 可以显示为：

```text
0 – 100
```

所有分数都应使用 `clamp(value, 0, 1)` 限制范围。

### 1.2 每个权重必须带置信度和来源

```yaml
WeightValue:
  value: float
  confidence: float
  parameter_source:
    - observed_from_data
    - inferred_proxy
    - assumption_driven
    - manual_parameter
    - mock_default
    - low_confidence
  notes: [string]
```

解释：

```text
observed_from_data：评论数、回复数、点赞数、转发数、时间戳等直接数据。
inferred_proxy：情绪强度、话题集中度、立场倾向、重复表达等公开行为代理。
assumption_driven：模型假设，例如身份绑定、逆反、真实私下立场等弱可观测变量。
manual_parameter：由分析师或 demo 手动设定。
mock_default：mock 场景默认值。
low_confidence：数据不足或推断弱。
```

禁止把公开行为代理说成真实心理测量。正确表达是：

> 系统根据公开发言、互动、时间、语义和传播行为，推断该事件中的行为特征代理指标。

---

## 2. Evidence Confidence / 证据置信权重

Evidence Confidence 是所有后续权重的底座。

### 2.1 输入字段

```text
provenance_type
verification_status
trust_label
review_status
duplicate_group_id
duplicate_count
risk_flags
source_url_present
```

### 2.2 基础分

```text
official_api_public:        0.95
official_api_oauth:         0.90
manual_url_with_source:     0.65
reviewed_public_parser:     0.60
user_upload:                0.45
vendor_attested:            0.45
search_candidate:           0.35
screenshot_transcription:   0.25
mock_fixture:               0.10
unknown:                    0.20
```

### 2.3 修正项

```text
approved:                   × 1.10
marked_weak:                × 0.70
needs_more_source:          × 0.60
rejected:                   × 0.00
duplicate_merged:           × 0.50
missing_source_url:         × 0.75
secret_redacted:            × 0.60
html_or_script_like_text:    × 0.60
source_unclear:             × 0.60
```

### 2.4 公式

```text
evidence_confidence = clamp(
  source_trust_base
  × review_multiplier
  × dedup_multiplier
  × source_url_multiplier
  × risk_penalty,
  0,
  1
)
```

### 2.5 作用

```text
低可信证据进入权重时自动降权。
被 reject 的证据默认不进入分析。
重复证据不能重复放大声量。
供应商样例默认 vendor_attested / medium_low，不升级为官方验证。
```

---

## 3. Influence Core Weight / 影响核心权重

Influence Core 是观念核心、叙事核心、内容核心。它不是人，而是能组织、吸附、放大、解释、极化或解构人群观点的内容或论点。

可以包括：

```text
KOL 发声
UP / 主播视频
自媒体文章
新闻报道
论坛串
爆火普通人内容
官方公告
第三方解释
社区梗 / 二创 / 歌曲 / 口号
```

### 3.1 `attention_weight` 注意力权重

表示该核心获得多少关注。

```text
attention_weight = clamp(
  log_scaled(
    views
    + likes * 0.5
    + comments * 2
    + replies * 2
    + shares * 3
    + citations * 3
  )
  × growth_factor
  × evidence_confidence,
  0,
  1
)
```

无播放量时，可用：

```text
comments
replies
shares
被引用次数
出现在多个集合体中的次数
```

### 3.2 `gravitational_pull` 吸附力

表示这个核心能不能把人群小球吸过去。

```text
gravitational_pull = clamp(
  0.30 * attention_weight
+ 0.20 * emotional_intensity
+ 0.20 * narrative_clarity
+ 0.15 * evidence_strength
+ 0.15 * source_credibility,
  0,
  1
)
```

解释：

```text
高热度 + 强情绪 + 论点清楚 + 有证据 + 来源可信 = 高吸附力。
普通人内容如果爆火，也可以有高吸附力。
```

### 3.3 `neutral_acceptance` 中立接受度

表示中立者是否容易接受这个核心。

```text
neutral_acceptance = clamp(
  0.30 * evidence_strength
+ 0.25 * logic_strength
+ 0.20 * source_credibility
+ 0.15 * tone_moderation
+ 0.10 * face_saving_score
- 0.25 * extremity_score
- 0.20 * autonomy_threat,
  0,
  1
)
```

注意：

```text
强情绪内容可能强化本阵营，但未必能吸引中立者。
证据强、逻辑清楚、语气温和、给台阶，通常更利于中立接受。
```

### 3.4 `same_camp_reinforcement` 本阵营强化力

```text
same_camp_reinforcement = clamp(
  0.30 * emotional_intensity
+ 0.25 * narrative_fit_to_camp
+ 0.20 * repetition_strength
+ 0.15 * source_alignment
+ 0.10 * community_validation,
  0,
  1
)
```

表示它能不能让本阵营更坚定。

### 3.5 `opponent_resistance` 对方抵抗度

```text
opponent_resistance = clamp(
  0.30 * extremity_score
+ 0.25 * autonomy_threat
+ 0.20 * identity_threat
+ 0.15 * perceived_dismissiveness
+ 0.10 * logical_vulnerability,
  0,
  1
)
```

高分含义：

```text
该核心可能稳住己方，但激怒对方。
该回应可能被认为冒犯、说教、狡辩、轻视问题。
```

### 3.6 `breakout_power` 破圈力

```text
breakout_power = clamp(
  0.30 * bridge_mentions
+ 0.25 * cross_platform_presence
+ 0.20 * non_core_audience_engagement
+ 0.15 * media_or_large_creator_entry
+ 0.10 * growth_velocity,
  0,
  1
)
```

表示该核心能不能让事件突破原 EchoBox。

### 3.7 `deconstruction_potential` 解构潜力

```text
deconstruction_potential = clamp(
  0.25 * meme_replicability
+ 0.20 * humor_acceptance
+ 0.20 * face_saving_score
+ 0.15 * community_co_creation_signal
+ 0.10 * fatigue_level
+ 0.10 * symbolic_flexibility
- 0.30 * harm_severity
- 0.25 * unresolved_responsibility,
  0,
  1
)
```

解释：

```text
解构潜力高，不代表一定建议解构。
如果事实未清、责任未处理、真实伤害高，解构应被禁止或强警告。
```

---

## 4. EchoBox Weight / 回音壁容器权重

EchoBox 是装着小球的框体，即一个有边界、有容量、有渗透率、有破圈风险的舆论生态箱。

### 4.1 `carrying_capacity` 容量上限

表示这个圈层最多能容纳多少关注或参与。

第一版不强求真实人数，可用等级：

```text
small / medium / large / very_large
```

估算公式：

```text
carrying_capacity_proxy = clamp(
  platform_base_reach
× creator_or_community_reach
× topic_general_interest
× bridge_potential,
  0,
  1
)
```

### 4.2 `saturation_ratio` 饱和度

```text
saturation_ratio = clamp(
  current_active_attention / estimated_carrying_capacity,
  0,
  1
)
```

解释：

```text
高饱和 + 低渗透 = 圈内爆炸，圈外无感。
低饱和 + 高渗透 = 还没爆，但容易破圈。
```

### 4.3 `permeability_score` 渗透率

```text
permeability_score = clamp(
  0.30 * bridge_node_density
+ 0.25 * non_core_audience_share
+ 0.20 * cross_platform_mentions
+ 0.15 * topic_general_interest
+ 0.10 * media_interest,
  0,
  1
)
```

表示外部路人是否容易进入。

### 4.4 `internal_reinforcement` 内部强化

```text
internal_reinforcement = clamp(
  0.30 * stance_homogeneity
+ 0.25 * same_camp_reply_ratio
+ 0.20 * repeated_claim_density
+ 0.15 * low_cross_cutting_exposure
+ 0.10 * high_emotion_density,
  0,
  1
)
```

高分含义：

```text
强回音壁。
同阵营互相强化。
外部观点难进入。
不代表全网大多数。
```

### 4.5 `breakout_risk` 破圈风险

```text
breakout_risk = clamp(
  0.30 * breakout_power_of_top_cores
+ 0.25 * permeability_score
+ 0.20 * growth_velocity
+ 0.15 * external_trigger_presence
+ 0.10 * media_or_kol_entry_risk,
  0,
  1
)
```

---

## 5. People Cluster Weight / 人群小球权重

People Cluster 是一小批相似人群或匿名参与者簇，不是实名用户。

### 5.1 `mobility` 可迁移性

```text
mobility = clamp(
  0.25 * low_stance_strength
+ 0.20 * evidence_sensitivity
+ 0.20 * low_identity_lock
+ 0.15 * low_public_commitment
+ 0.10 * fatigue
+ 0.10 * high_information_gap,
  0,
  1
)
```

高 mobility 的小球更容易转中立、转温和支持、转温和反对或退出。

### 5.2 `identity_lock` 核心锁定

```text
identity_lock = clamp(
  0.30 * stance_strength
+ 0.25 * repeated_same_stance
+ 0.20 * community_identity_signal
+ 0.15 * public_commitment
+ 0.10 * conflict_history,
  0,
  1
)
```

高 identity_lock 的小球不应轻易变色。

### 5.3 `evidence_sensitivity` 证据敏感度

```text
evidence_sensitivity = clamp(
  0.30 * reasoning_language_ratio
+ 0.25 * question_asking_ratio
+ 0.20 * source_request_behavior
+ 0.15 * lower_emotional_intensity
+ 0.10 * stance_moderation,
  0,
  1
)
```

用途：

```text
区分更吃事实、逻辑、来源说明的人群。
```

### 5.4 `emotion_load` 情绪负载

```text
emotion_load = clamp(
  0.35 * sentiment_intensity
+ 0.25 * anger_or_mockery_signal
+ 0.20 * exclamation_attack_density
+ 0.10 * repetition_score
+ 0.10 * reply_conflict_intensity,
  0,
  1
)
```

### 5.5 `fatigue` 讨论疲劳

```text
fatigue = clamp(
  0.30 * declining_post_frequency
+ 0.25 * declining_reply_depth
+ 0.20 * time_since_peak
+ 0.15 * repeated_topic_exhaustion
+ 0.10 * attention_shift_to_other_topics,
  0,
  1
)
```

### 5.6 `grievance_memory` 潜伏不满 / 反噬记忆

```text
grievance_memory = clamp(
  0.30 * unresolved_core_claim
+ 0.25 * high_emotion_load
+ 0.20 * withdrawal_without_neutralization
+ 0.15 * perceived_unfairness
+ 0.10 * prior_similar_event_reference,
  0,
  1
)
```

这解释：

```text
声量下降不等于问题解决。
退出讨论不等于理解或和解。
```

### 5.7 `face_saving_need` 台阶需求

```text
face_saving_need = clamp(
  0.35 * public_commitment_level
+ 0.25 * prior_attack_intensity
+ 0.20 * peer_visibility
+ 0.10 * identity_lock
+ 0.10 * ridicule_risk_if_switch,
  0,
  1
)
```

高分意味着：

```text
即使该群体理解了事实，也不容易公开改口。
需要第三方解释、梗化缓冲、低冲突退出路径。
```

---

## 6. Camp Dynamics Score / 阵营迁移分数

这些不是严格因果概率，第一版应称为 score 或 scenario likelihood。

### 6.1 `neutralization_score` 中立化可能

```text
neutralization_score = clamp(
  mobility
× neutral_acceptance
× face_saving_score
× evidence_confidence
× timing_fit
× (1 - opponent_resistance),
  0,
  1
)
```

适用对象：

```text
oppose_soft
neutral_engaged
support_soft
```

不应直接适用：

```text
oppose_core
oppose_extreme
support_core
```

### 6.2 `conversion_score` 同化可能

```text
conversion_score = clamp(
  mobility
× gravitational_pull
× narrative_fit
× source_trust
× repeated_exposure
× (1 - identity_lock),
  0,
  1
)
```

转换应分阶段：

```text
oppose_soft → neutral_engaged → support_soft
support_soft → neutral_engaged → oppose_soft
neutral_observing → neutral_engaged → support_soft / oppose_soft
```

### 6.3 `withdrawal_score` 退出可能

```text
withdrawal_score = clamp(
  fatigue
× low_new_information
× low_social_reward
× time_since_peak
× saturation_ratio,
  0,
  1
)
```

退出后必须继续记录：

```text
grievance_memory
reactivation_risk
```

### 6.4 `hardening_score` 固化 / 极化可能

```text
hardening_score = clamp(
  internal_reinforcement
× same_camp_reinforcement
× emotion_load
× perceived_opponent_threat
× echo_chamber_score,
  0,
  1
)
```

### 6.5 `backlash_score` 反噬可能

```text
backlash_score = clamp(
  opponent_resistance
× unresolved_responsibility
× autonomy_threat
× perceived_dismissiveness
× high_emotion_load
× poor_timing,
  0,
  1
)
```

### 6.6 `reactivation_risk` 再激活风险

```text
reactivation_risk = clamp(
  grievance_memory
× similar_future_trigger_probability
× meme_persistence
× unresolved_claim_strength
× low_trust_recovery,
  0,
  1
)
```

---

## 7. Case Severity Gate / 事件严重度闸门

在推荐解构、梗化、自嘲或社区和解之前，必须先过严重度闸门。

```yaml
CaseSeverity:
  harm_level:
    - low
    - medium
    - high
    - severe
  responsibility_level:
    - none
    - contested
    - partial
    - high
    - unknown
  factual_clarity: float
  remedy_progress: float
  apology_status:
    - none
    - weak
    - adequate
    - strong
    - not_needed
  deconstruction_allowed: bool
```

规则：

```text
真实伤害高 → 不建议解构，除非已经充分处理责任和补救。
事实不清 → 不建议解构。
责任未处理 → 不建议解构。
未成年人、公共安全、违法、严重受害者场景 → 强限制解构。
```

---

## 8. Case Lifecycle / 事件生命周期

```text
seed       种子期
rise       上升期
peak       峰值期
plateau    高位平台期
fatigue    疲劳期
decay      衰退期
archive    档案期 / 长期标签期
reactive   再激活期
```

生命周期影响处理节奏：

```text
seed / rise：优先解释事实，防止错误叙事定型。
peak：止血，避免高压和情绪对撞。
plateau：判断是否破圈，识别核心论点和软反对者。
fatigue：可考虑低强度降压、第三方解释、解构窗口。
decay：监测退出与潜伏不满。
archive：关注长期污名和梗化残留。
reactive：历史 grievance_memory 重新激活。
```

---

## 9. Response Tempo Score / 处理节奏分数

最终输出不是单一方案，而是节奏判断。

### 9.1 `clarification_priority` 澄清优先级

```text
clarification_priority = clamp(
  information_gap
× neutral_engaged_share
× evidence_sensitivity
× breakout_risk,
  0,
  1
)
```

高分：需要尽快解释事实、时间线、责任边界。

### 9.2 `faq_priority` FAQ 优先级

```text
faq_priority = clamp(
  repeated_questions
× topic_confusion
× neutral_observing_share
× low_to_medium_emotion_load,
  0,
  1
)
```

### 9.3 `third_party_explanation_priority` 第三方说明优先级

```text
third_party_explanation_priority = clamp(
  low_official_trust
× high_expert_or_media_trust
× evidence_sensitivity
× neutral_acceptance_gap,
  0,
  1
)
```

### 9.4 `deconstruction_window_score` 解构窗口分

```text
deconstruction_window_score = clamp(
  fatigue
× soft_oppose_share
× neutral_engaged_share
× meme_replicability
× face_saving_score
× factual_clarity
× remedy_progress
- backlash_risk
- long_term_stigma_risk,
  0,
  1
)
```

### 9.5 `wait_and_monitor_score` 观察等待分

```text
wait_and_monitor_score = clamp(
  high_saturation_ratio
× low_permeability
× declining_growth_velocity
× low_breakout_risk
× high_fatigue,
  0,
  1
)
```

高分说明：

```text
可能是圈内高热但外溢弱，过度回应可能反而扩圈。
```

---

## 10. Reputation Memory / 长期声誉残留

事件结束后不应清零。

```yaml
ReputationMemory:
  case_id: string
  subject_id: string | null
  stigma_tags: [string]
  unresolved_grievance_score: float
  meme_persistence: float
  trust_recovery: float
  reactivation_triggers: [string]
  next_event_sensitivity: float
```

用途：

```text
识别长期黑称。
识别未来相似事件再激活风险。
区分短期降温和真正理解 / 和解。
```

---

## 11. UI / 报告展示原则

### 11.1 用区间，不用确定预言

推荐表达：

```text
在当前证据和假设下，温和反对者中立化窗口为中等偏高。
预计中立参与者更可能受事实说明影响，而非情绪化回应影响。
```

避免表达：

```text
9.6% 的反对者一定会转支持。
某节点导致某阵营改变。
```

### 11.2 显示覆盖边界

必须显示：

```text
当前结果基于已导入 / 可用证据和模型假设，不代表全网全量覆盖，也不代表因果确定。
```

### 11.3 显示数据来源标签

每个主要分数应显示：

```text
数据观测
公开行为代理
模型假设
手动参数
mock 默认
低置信
```

---

## 12. MVP 实现路线

### Phase 0：文档冻结

```text
本文件作为 research/design 文档入库。
不声称代码已实现。
```

### Phase 1：schema-only mock

```text
定义 WeightValue。
定义 EvidenceConfidence。
定义 InfluenceCoreWeight。
定义 EchoBoxWeight。
定义 PeopleClusterWeight。
定义 CampDynamicsScore。
定义 ResponseTempoScore。
使用 mock fixtures 生成结果。
不调用真实 API。
不接 LLM。
```

### Phase 2：frontend-only mock 小球沙盒

```text
100–300 个小球。
一个或多个 EchoBox。
Influence Core 作为引力核心。
小球颜色、大小、速度、透明度、边框变化。
播放 / 暂停 / 重置 / 场景切换。
```

### Phase 3：Evidence → Weight 映射

```text
从 EvidenceItem 聚合 Influence Core。
从 EvidenceItem 聚合 People Cluster。
从 source_url / aggregate 生成 EchoBox。
从 trust / review / dedup 调整权重。
```

### Phase 4：真实 demo 数据

```text
真实事件。
合规导入数据：CSV/Excel、Manual URL、可选 YouTube、供应商样例。
不等同 live API。
明确 coverage note。
```

---

## 13. Codex 暂不建议直接做的任务

除非用户明确要求并完成前置设计，不要让 Codex 直接做：

```text
真实平台 API 接入
真实 RSS/GDELT/Search provider
真实 vendor adapter
真实 LLM social simulation
MediaCrawler integration
OpenClaw production ingestion
个人级 persuasion ranking
bot / 水军模拟模块
自动判定某人是水军 / 串子
```

推荐的第一步 Codex 任务应是：

```text
docs-only：新增本文件。
或 backend schema-only：mock weight schemas，不调用外部 API。
或 frontend-only：mock 小球沙盒视觉原型，不接真实数据。
```

---

## 14. 仍需后续讨论的问题

```text
1. 哪些变量第一版从数据估计，哪些只做 mock_default？
2. Influence Core 的生成阈值如何设定？
3. EchoBox 的 carrying_capacity 第一版用等级还是数值？
4. 小球公开页默认显示 cluster，B 端是否允许 actor drill-down？
5. 真实 demo 选择哪个游戏 / 动漫 / 社区争议？
6. 是否需要生成新的 Project Source 09？
```

当前建议：

```text
先把本文件作为 repo research 文档保留。
暂不替换 Project Source。
等模型稳定并进入实现阶段，再考虑新增 Source 09 或替换 Source 08。
```
