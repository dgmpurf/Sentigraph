# Sentigraph Evidence → Opinion Ecosystem Mapping v1

**更新时间**：2026-06-13  
**用途**：定义 Sentigraph 现有 Evidence Layer 如何映射到下一阶段 Opinion Ecosystem Model，包括 Influence Core、EchoBox、People Cluster、Camp Dynamics、Deconstruction Core、Response Tempo 与 Reputation Memory。  
**性质**：research/design 文档；不代表当前代码已经实现这些映射。  
**适用阶段**：Phase 3 设计阶段。Phase 1/2 已完成 frontend-only mock sandbox 与 frontend-local mock schema；本文件用于 Phase 3 之前的模型映射约束。  

---

## 0. 状态声明

当前 Sentigraph 已经具备：

```text
EvidenceItem
Evidence Trust / Provenance / Deduplication
Evidence Review Queue
Audit Timeline
Evidence Scale / Coverage
CSV / Excel Import
Manual URL Evidence
YouTube optional official API path
Search Discovery mock/static
Vendor sample POC utilities
Analysis / Report / Forecast / Simulation Lab
Opinion Ecosystem Sandbox frontend mock visual prototype
Opinion Ecosystem frontend-local mock schema
```

当前仍未正式实现：

```text
EvidenceItem → Influence Core 自动映射
EvidenceItem → EchoBox 自动映射
EvidenceItem → People Cluster 自动映射
真实 Camp Dynamics 计算
真实 Response Tempo 计算
真实 Reputation Memory 计算
真实 case calibration
真实平台多源 live adapter
真实 LLM simulation
```

本文件的目的不是让 Codex 立即写生产功能，而是先固定：

```text
现有 Evidence 数据怎么进入舆论生态模型；
哪些证据可以形成 Influence Core；
哪些证据只能形成 People Cluster 或 supporting reference；
trust / review / dedup 如何影响权重；
哪些情况必须降级、复核或标注不确定性。
```

---

## 1. 不改变的项目边界

本文件不改变 Sentigraph 当前边界：

```text
Sentigraph 不是全网自动爬虫。
当前真实官方 API 路径只有可选 YouTube。
CSV/Excel、Manual URL、Search Discovery、Vendor POC 都是 Evidence 入口。
Search Discovery / RSS / GDELT 当前是 mock/static，不是 live provider。
供应商数据默认 vendor_attested / medium_low，不是官方验证。
MediaCrawler 不集成主线。
OpenClaw/龙虾只能作为外部人工辅助工具。
抖音/B站/小红书/Reddit/微博等真实接入仍 pending。
LLM 仍是 mock。
Evidence Scale / Coverage 不代表全网全量覆盖。
```

本文件新增的是：

```text
Evidence Layer 之上的 Opinion Ecosystem 映射规则。
```

禁止将本文件解释为：

```text
已经接入真实抖音/B站/小红书/微博 API
已经可以全网自动抓取
已经实现真实 RSS/GDELT/search provider
已经实现真实 vendor adapter
已经实现真实小球 agent simulation
已经可以个人级 persuasion scoring
```

---

## 2. 目标链路

Opinion Ecosystem Model 的目标链路是：

```text
EvidenceItem
→ EvidenceRole
→ SourceIdentity
→ Influence Core / Narrative Core
→ EchoBox
→ People Cluster
→ Camp Dynamics
→ Deconstruction Core
→ Case Lifecycle
→ Response Tempo
→ Reputation Memory
```

解释：

```text
EvidenceItem：
现有 Sentigraph 统一证据记录。

EvidenceRole：
判断这条证据在生态模型中扮演什么角色。

SourceIdentity：
发布者 / 来源身份，例如 KOL、UP、媒体、官方、普通用户、组织等。
注意：SourceIdentity 不是 PeopleCluster 小球。

Influence Core：
观念核心 / 影响核心，例如 KOL 视频、媒体文章、官方公告、爆火普通内容、话题主张、社区梗。

EchoBox：
回音壁容器 / 舆论生态箱，表示某个圈层、平台、集合体或讨论场的边界、容量、渗透率和破圈风险。

People Cluster：
一小批相似人群 / 匿名参与者簇。C 端公开展示默认使用 cluster，不展示个人级 actor。

Camp Dynamics：
阵营迁移规则，包括同化、中立化、退出、固化、反噬、潜伏再激活。

Deconstruction Core：
特殊 Influence Core，用于叙事降压、梗化重构、社区和解、符号再编码。

Case Lifecycle：
事件生命周期阶段，例如 seed / rise / peak / fatigue / decay / archive / reactive。

Response Tempo：
处理节奏建议，例如澄清、FAQ、第三方解释、等待观察、解构窗口、反噬预警。

Reputation Memory：
长期声誉残留，例如黑称、未解决不满、信任恢复、未来再激活风险。
```

---

## 3. EvidenceItem 输入字段需求

现有 EvidenceItem 已经可以承接很多字段。Phase 3 映射至少需要以下字段。

### 3.1 标识与来源

```yaml
evidence_id: string
case_id: string
platform: string
source_type: string
acquisition_mode: string
provenance_type: string
verification_status: string
trust_label: string
trust_score: float
review_status: string
source_url: string | null
url: string | null
```

### 3.2 内容结构

```yaml
evidence_type:
  - video
  - post
  - article
  - thread
  - comment
  - reply
  - search_result
  - uploaded_record
  - manual_text
  - screenshot_transcription
  - mock_fixture

title: string | null
body_text: string | null
comment_text: string | null
claim_summary: string | null
root_id: string | null
parent_id: string | null
source_root_id: string | null
```

### 3.3 作者与身份

```yaml
author_id: string | null
author_name: string | null
author_type:
  - ordinary_user
  - creator
  - up
  - kol
  - streamer
  - media
  - expert
  - official
  - organization
  - unknown
```

### 3.4 互动指标

```yaml
view_count: number | null
like_count: number | null
reply_count: number | null
comment_count: number | null
share_count: number | null
favorite_count: number | null
repost_count: number | null
quote_count: number | null
created_at: datetime | null
captured_at: datetime | null
```

### 3.5 治理字段

```yaml
content_hash: string | null
normalized_content_hash: string | null
canonical_url_hash: string | null
duplicate_group_id: string | null
duplicate_count: int
risk_flags: [string]
review_history: [object]
```

---

## 4. EvidenceRole：先判断证据角色

每条 EvidenceItem 在进入生态模型前，先被分配一个 `evidence_role`。

```yaml
EvidenceRole:
  evidence_id: string
  role:
    - candidate_influence_core
    - people_expression
    - supporting_reference
    - deconstruction_candidate
    - echo_box_boundary_signal
    - source_identity_signal
    - unknown_or_unusable
  role_confidence: float
  role_reason: string
```

### 4.1 candidate_influence_core

可以成为 Influence Core 的证据。

典型情况：

```text
视频
文章
帖子
论坛串
媒体报道
官方公告
KOL / UP / 主播发声
爆火普通人内容
被多处引用的截图 / 片段 / 标题 / 观点
```

满足以下任意多项时优先提升：

```text
有高互动指标
短时间增长快
被多个证据引用
由官方 / 媒体 / 专家 / 高影响 creator 发布
是事件导火索
是二次爆发源
形成某阵营核心论点
```

### 4.2 people_expression

用于形成 People Cluster 的证据。

典型情况：

```text
评论
回复
用户上传的评论记录
Manual text 中的单条发言
供应商样例中的评论或发言
```

这些通常不直接形成 Influence Core，除非它们爆火、被引用、形成导火索。

### 4.3 supporting_reference

用于支持、验证、解释 Influence Core 或 Response Tempo 的证据。

典型情况：

```text
新闻链接
公告链接
事实说明
第三方报告
FAQ
Manual URL
公开来源说明
```

### 4.4 deconstruction_candidate

用于形成 Deconstruction Core 的证据。

典型情况：

```text
梗图
二创视频
自嘲歌曲
社区口号
反讽式回应
轻量解释视频
仪式化短语
长期传播黑称
```

### 4.5 echo_box_boundary_signal

用于判断 EchoBox 边界和容量。

典型情况：

```text
同平台同集合体大量评论
同贴吧 / 论坛 / 社区串
同 UP 评论区
同话题标签
同社区多次重复表达
跨平台搬运迹象
外圈 KOL / 媒体介入迹象
```

### 4.6 unknown_or_unusable

无法稳定映射或必须排除的证据。

典型情况：

```text
被 review rejected
缺少内容且缺少来源
疑似 secret / token / 私密信息
mock fixture 被误用于真实 demo
严重低可信且无复核
```

---

## 5. 证据治理门控

所有映射必须先经过 trust / review / dedup 门控。

### 5.1 review_status 门控

```text
rejected:
  默认不进入 Influence Core、People Cluster、EchoBox 权重。
  可在审计中保留。

marked_weak:
  可进入，但权重降级，并在输出中显示 weak evidence warning。

needs_more_source:
  可进入 low-confidence 映射，但不能作为核心结论。

approved:
  可正常进入，但仍保留原 provenance 和 verification。

not_reviewed / review_needed:
  可进入初步分析，但应标注低置信或待复核。
```

### 5.2 duplicate 门控

```text
同一 duplicate_group_id 内只用主证据参与主计数。
duplicate_count 作为重复信号，不直接放大声量。
重复表达可以提高 repetition_score，但不能提高 unique participation。
```

### 5.3 source trust 门控

默认建议：

```text
official_api_public:
  高置信，适合形成高可信 Influence Core / PeopleCluster 输入。

manual_url:
  中等置信，需要 source_url 和 attestation。

user_upload:
  medium_low，需要复核和去重。

data_vendor:
  vendor_attested / medium_low 默认，不等于官方验证。

search_discovery_candidate:
  unverified / needs_review，不可当作真实搜索结果。

mock_fixture:
  仅用于 demo 和测试，不可用于真实 demo 结论。

screenshot_transcription:
  low / unverified，不能自动视为真实。
```

### 5.4 风险标记

包含以下 risk_flags 时必须降权或复核：

```text
source_unclear
missing_source_url
external_agent_assisted
screenshot_unverified
secret_redacted
html_script_like
vendor_source_unclear
duplicate_group
private_or_sensitive
```

---

## 6. SourceIdentity 映射

SourceIdentity 表示“谁发布 / 承载了影响核心”，但它不是 PeopleCluster 小球。

```yaml
SourceIdentity:
  source_id: string
  case_id: string
  platform: string
  source_type:
    - ordinary_user
    - creator
    - up
    - kol
    - streamer
    - media
    - expert
    - official
    - organization
    - community
    - unknown
  platform_source_hash: string
  display_label_policy:
    public_label: string
    show_public_name: bool
    anonymize_in_public_demo: bool
  credibility:
    source_credibility: float
    credibility_confidence: float
    parameter_source: string
  audience_base_alignment:
    support: float
    neutral: float
    oppose: float
    unknown: float
```

### 6.1 映射规则

```text
如果 author_type 是 media / official / expert / organization：
  生成 SourceIdentity，source_type 对应。

如果 EvidenceItem 是 creator/up/kol/streamer 发布内容：
  生成 SourceIdentity，并关联到 Influence Core。

如果普通用户内容爆火：
  生成 ordinary_user SourceIdentity，但公开 demo 默认匿名。

如果只有 author_name 没有 author_id：
  可生成 weak_source_hash，confidence 降级。

如果 author 信息缺失：
  source_type=unknown，不生成稳定 source identity。
```

### 6.2 重要边界

```text
SourceIdentity 不等于真实身份。
默认不做跨平台个人识别。
公开 C 端展示默认匿名化。
B 端也不展示原始 uid / 用户名，除非用户合法提供并用于内部复核。
```

---

## 7. Influence Core 映射

Influence Core 是观念核心 / 影响核心，不是小球。

```yaml
InfluenceCore:
  core_id: string
  case_id: string
  core_type:
    - kol_statement
    - creator_video
    - creator_post
    - media_article
    - news_report
    - forum_thread
    - viral_ordinary_content
    - official_statement
    - third_party_explanation
    - community_meme
    - topic_claim
    - unknown
  source_identity_id: string | null
  evidence_ids: [string]
  source_url: string | null
  platform: string
  label: string
  stance_label: [support, neutral, oppose, mixed, unknown]
  stance_score: float
  stance_strength: float
  narrative:
    claim_summary: string
    evidence_strength: float
    logic_strength: float
    logical_vulnerability: float
    emotional_intensity: float
    extremity_score: float
  influence_weights:
    attention_weight: float
    gravitational_pull: float
    neutral_acceptance: float
    same_camp_reinforcement: float
    opponent_resistance: float
    bridge_power: float
    breakout_power: float
    deconstruction_potential: float
  confidence:
    evidence_confidence: float
    parameter_source: string
```

### 7.1 生成 Influence Core 的条件

第一版建议采用阈值 + 规则组合：

```text
1. 内容主体型：
   evidence_type in [video, post, article, thread]
   且有 source_url/root_id/title/body_text。

2. 权威来源型：
   author_type in [official, media, expert, organization]
   即使互动不高，也可成为核心候选。

3. 高传播型：
   view/like/comment/share/repost 任一指标达到当前 case 分位阈值。

4. 高引用型：
   被多个 people_expression 引用或复述。

5. 导火索型：
   created_at 接近事件爆发点，且后续大量讨论引用它。

6. 阵营核心型：
   某一阵营大量围绕该内容形成一致主张。

7. 解构候选型：
   meme / parody / self-mockery / music / ritual_phrase 等形式。
```

### 7.2 不应生成 Influence Core 的情况

```text
普通低互动评论
缺少来源和上下文的截图转录
低可信供应商片段
已被 reject 的证据
重复导入的同一内容
mock fixture 被用于真实 demo
```

### 7.3 Influence Core 类型映射

```text
official statement:
  author_type=official 或 organization，core_type=official_statement

media article:
  author_type=media，evidence_type=article/news_report

creator video:
  author_type=up/kol/creator/streamer，evidence_type=video

viral ordinary content:
  author_type=ordinary_user，但互动/引用/增长极高

topic claim:
  多条 evidence 重复表达同一核心主张，但没有单一源头

community meme:
  出现短语、梗、二创、重复口号、符号再编码
```

---

## 8. EchoBox 映射

EchoBox 是回音壁容器，不是 UI 背景。

```yaml
EchoBox:
  box_id: string
  case_id: string
  label: string
  platform: string
  box_type:
    - aggregate_box
    - platform_box
    - topic_box
    - creator_audience_box
    - cross_platform_box
    - external_media_box
    - unknown
  aggregate_ids: [string]
  influence_core_ids: [string]
  people_cluster_ids: [string]
  boundary:
    echo_chamber_score: float
    carrying_capacity: float
    saturation_ratio: float
    permeability_score: float
    breakout_risk: float
  dynamics:
    internal_reinforcement: float
    external_inflow_rate: float
    fatigue_rate: float
    growth_velocity: float
    decay_rate: float
  lifecycle_stage:
    - seed
    - rise
    - peak
    - plateau
    - fatigue
    - decay
    - archive
    - reactive
  confidence:
    data_confidence: float
    parameter_source: string
```

### 8.1 EchoBox v1 生成规则

```text
默认 case-level EchoBox：
  每个 case 至少一个总 EchoBox。

aggregate_box：
  按 canonical source_url / root_id / thread_id 生成。

platform_box：
  同一平台下多个 aggregate 有强关联时生成。

topic_box：
  同一 topic_claim 被多个 aggregate 讨论时生成。

creator_audience_box：
  某 KOL/UP/媒体受众围绕某 Influence Core 形成讨论时生成。

cross_platform_box：
  仅在明确出现跨平台引用 / 搬运 / 媒体扩散证据时生成。
```

### 8.2 EchoBox 边界判断

```text
高 echo_chamber_score：
  stance_homogeneity 高
  internal_reinforcement 高
  cross_cutting_exposure 低
  repeated_claim_density 高

高 permeability_score：
  bridge_node_density 高
  non_core_audience_share 高
  cross_platform_mentions 高
  topic_general_interest 高

高 breakout_risk：
  top Influence Core breakout_power 高
  外部 KOL/媒体介入
  growth_velocity 高
  EchoBox 边界出现跨圈层通道
```

### 8.3 容量上限注意

`carrying_capacity` 不是全网人数。  
第一版只能做 proxy：

```text
小圈层
中等圈层
大圈层
极大圈层
```

公开输出必须写：

```text
这是基于已导入证据和模型假设的估计，不代表全平台全量覆盖。
```

---

## 9. People Cluster 映射

People Cluster 表示一小批人 / 匿名参与者簇。

```yaml
PeopleCluster:
  cluster_id: string
  case_id: string
  echo_box_id: string
  source_actor_hashes: [string]
  evidence_ids: [string]
  label: string
  camp_state:
    - support_core
    - support_soft
    - neutral_observing
    - neutral_engaged
    - oppose_soft
    - oppose_core
    - oppose_extreme
    - withdrawn
    - dormant_grievance
  stance_label: [support, neutral, oppose, mixed, unknown]
  stance_score: float
  stance_strength: float
  population_weight: float
  behavior_weights:
    mobility: float
    identity_lock: float
    evidence_sensitivity: float
    emotion_load: float
    fatigue: float
    grievance_memory: float
    deconstruction_receptivity: float
    social_cost_to_switch: float
    influence_weight: float
    activity_weight: float
    expression_intensity: float
  confidence:
    data_confidence: float
    parameter_source: string
```

### 9.1 从作者生成匿名 actor key

```text
如果 author_id 存在：
  platform + hash(author_id + case_id_salt) → platform_actor_hash

如果只有 author_name：
  platform + hash(author_name + case_id_salt) → weak_actor_hash
  confidence 降级

如果没有 author_id / author_name：
  不生成稳定 actor，只进入 anonymous_unknown bucket
```

### 9.2 从 actor 到 cluster

C 端默认不显示单个 actor，而显示 cluster。

第一版聚合规则：

```text
platform
+ echo_box_id
+ stance_label
+ camp_state
+ dominant_topic
+ similar behavior weights
```

示例：

```text
核心玩家反对簇
证据敏感中立簇
情绪化温和反对簇
支持方基本盘簇
路人围观簇
潜伏不满簇
```

### 9.3 camp_state 判断

```text
support_core:
  stance_score 高正，stance_strength 高，identity_lock 高。

support_soft:
  stance_score 正，但 stance_strength 中低，mobility 中高。

neutral_observing:
  stance_score 接近 0，activity 低，expression_intensity 低。

neutral_engaged:
  stance_score 接近 0，但 activity / question / reasoning 高。

oppose_soft:
  stance_score 负，stance_strength 中低，mobility 中高。

oppose_core:
  stance_score 高负，stance_strength 高，identity_lock 高。

oppose_extreme:
  stance_score 高负，emotion_load 高，extremity / attack / conflict signal 高。

withdrawn:
  历史参与后 activity 明显下降，fatigue 高。

dormant_grievance:
  activity 下降，但 grievance_memory 高，未解决核心主张仍强。
```

### 9.4 边界

People Cluster 权重是公开行为代理，不是真实心理测量。

禁止输出：

```text
这个人最容易被说服
这个人真实心理是……
这个账号一定是水军
这个用户真实身份是……
```

允许输出：

```text
该人群簇表现出较高证据敏感度代理指标。
该人群簇处于温和反对状态，存在中立化窗口。
该人群簇退出讨论但残留不满风险较高。
```

---

## 10. Camp Dynamics 映射

Camp Dynamics 不是直接从单条 Evidence 生成，而是由 Influence Core、EchoBox、People Cluster 的权重共同计算。

```yaml
CampDynamics:
  case_id: string
  echo_box_id: string
  scenario_id: string
  camp_distribution:
    support_core: float
    support_soft: float
    neutral_observing: float
    neutral_engaged: float
    oppose_soft: float
    oppose_core: float
    oppose_extreme: float
    withdrawn: float
    dormant_grievance: float
  transition_scores:
    conversion_score: float
    neutralization_score: float
    withdrawal_score: float
    hardening_score: float
    backlash_score: float
    reactivation_risk: float
  confidence:
    data_confidence: float
    parameter_source: string
```

### 10.1 基本转移

```text
Assimilation / 同化：
  oppose_soft → neutral_engaged → support_soft
  support_soft → neutral_engaged → oppose_soft

Neutralization / 中立化：
  oppose_soft → neutral_observing / neutral_engaged

Withdrawal / 退出：
  neutral_engaged / oppose_soft / support_soft → withdrawn

Hardening / 固化：
  support_soft → support_core
  oppose_soft → oppose_core
  oppose_core → oppose_extreme

Backlash / 反噬：
  neutral_observing → oppose_soft
  support_soft → neutral_engaged / oppose_soft

Dormant Reactivation / 潜伏再激活：
  withdrawn / dormant_grievance → oppose_soft / oppose_core
```

### 10.2 重要限制

```text
核心派不应轻易直接变色。
极端派通常只会强化、退出或再激活，不直接被同化。
中立者、温和派、证据敏感群体、疲劳群体是主要迁移对象。
```

---

## 11. Deconstruction Core 映射

Deconstruction Core 是特殊 Influence Core，用于叙事降压 / 符号重构 / 梗化 / 社区和解。

```yaml
DeconstructionCore:
  core_id: string
  case_id: string
  target_core_id: string | null
  target_narrative: string
  deconstruction_type:
    - self_mockery
    - meme_reframe
    - parody
    - music_video
    - community_co_creation
    - third_party_humor
    - ritual_phrase
    - neutral_explainer
    - unknown
  effects:
    threat_deflation: float
    humor_acceptance: float
    face_saving_score: float
    neutralization_power: float
    conversion_power: float
    withdrawal_power: float
    ridicule_persistence: float
    meme_replicability: float
    community_co_creation: float
    backlash_risk: float
    long_term_stigma_risk: float
  deconstruction_fit_score: float
  confidence:
    data_confidence: float
    parameter_source: string
```

### 11.1 候选证据

```text
梗图
二创视频
自嘲歌曲
社区口号
高重复仪式化短语
轻量解释视频
当事人或第三方的低冲突再表达
```

### 11.2 解构前置门

必须先经过 CaseSeverity 判断。

```text
如果 harm_level 高，responsibility_level 未清，remedy_progress 低：
  不建议解构。

如果 factual_clarity 低：
  不建议解构。

如果处于 peak 强冲突阶段：
  通常不建议强行解构。

如果进入 fatigue / post_peak，温和反对者和中立参与者疲劳上升：
  可进入低强度解构观察。
```

---

## 12. Case Lifecycle 映射

Case Lifecycle 用于判断处理节奏。

```yaml
CaseLifecycle:
  case_id: string
  stage:
    - seed
    - rise
    - peak
    - plateau
    - fatigue
    - decay
    - archive
    - reactive
  attention_curve:
    current_attention: float
    growth_velocity: float
    peak_distance: float
    decay_rate: float
  evidence:
    first_seen_at: datetime | null
    last_seen_at: datetime | null
    peak_estimated_at: datetime | null
  confidence:
    data_confidence: float
    parameter_source: string
```

第一版规则：

```text
seed:
  evidence 少，增长刚开始。

rise:
  growth_velocity 高，外部参与增加。

peak:
  attention 高，情绪强，正反冲突高。

plateau:
  attention 高但增长放缓，争论持续。

fatigue:
  activity 下降，reply depth 降低，重复话题增加。

decay:
  attention 明显下降，新增证据少。

archive:
  事件变成长期标签、梗、黑称或记忆。

reactive:
  旧事件被新证据 / 新争议重新激活。
```

---

## 13. Response Tempo 映射

Response Tempo 是最终处理节奏建议，不是执行动作。

```yaml
ResponseTempo:
  case_id: string
  scenario_id: string
  clarification_priority: float
  faq_priority: float
  third_party_explanation_priority: float
  deconstruction_window_score: float
  wait_and_monitor_score: float
  recommendation_label:
    - clarify_now
    - prepare_faq
    - use_third_party_explanation
    - monitor_before_response
    - prepare_low_intensity_deconstruction
    - avoid_deconstruction
    - backlash_watch
  recommendation_text: string
  risk_notes: [string]
  confidence:
    data_confidence: float
    parameter_source: string
```

### 13.1 输出示例

```text
当前更适合补充事实说明，不建议强行解构。
温和反对者存在中立化窗口。
中立参与者仍在观察，FAQ 价值较高。
当前 EchoBox 高热但外溢弱，过度回应可能反而扩圈。
声量下降不等于问题解决，存在潜伏反噬风险。
```

### 13.2 禁止输出

```text
找谁带节奏
怎么压制对方
怎么制造声量
怎么批量举报
怎么暗中投放 KOL
怎么操控中立人群
```

---

## 14. Reputation Memory 映射

Reputation Memory 表示事件结束后的长期残留。

```yaml
ReputationMemory:
  case_id: string
  unresolved_grievance_score: float
  stigma_tags: [string]
  stigma_persistence: float
  meme_persistence: float
  trust_recovery: float
  reactivation_risk: float
  reactivation_triggers: [string]
  monitoring_notes: [string]
  confidence:
    data_confidence: float
    parameter_source: string
```

### 14.1 作用

它回答：

```text
事件是不是只是声量下降？
有没有留下长期黑称？
有没有未解决不满？
下次类似事件会不会被翻旧账？
梗化是降低攻击性，还是固化污名？
```

---

## 15. 降级策略

映射时必须处理数据缺失。

### 15.1 缺少 author_id

```text
使用 author_name 生成 weak hash。
confidence 降级。
公开展示默认进入 cluster，不展示单 actor。
```

### 15.2 缺少 source_url

```text
如果有 root_id / platform / title：
  可形成弱 aggregate / EchoBox。

如果都没有：
  进入 unknown_evidence_bucket。
  不生成高置信 Influence Core。
```

### 15.3 缺少互动指标

```text
attention_weight 使用 comment_count / evidence_count / citation_count proxy。
标记 parameter_source=inferred_proxy 或 low_confidence。
```

### 15.4 低可信证据

```text
低可信证据可以作为弱信号，但不能支撑高置信结论。
```

### 15.5 mock 数据

```text
mock_fixture 只能进入 demo / test 模式。
真实 demo 和报告必须显式排除或标注。
```

---

## 16. C 端与 B 端展示差异

### C 端公开页

默认展示：

```text
EchoBox
People Cluster
Influence Core 摘要
正 / 中 / 反分布
热区
破圈风险
处理节奏摘要
覆盖边界
不确定性提示
```

不展示：

```text
单个 actor
原始 uid
精细个人行为评分
敏感证据
未复核低可信证据细节
```

### B 端私有报告

可以展示：

```text
更细 PeopleCluster 权重
匿名 actor drill-down
Influence Core 证据链
EchoBox 破圈判断
Response Tempo 风险说明
Reputation Memory
```

仍不展示或不默认展示：

```text
真实身份推断
跨平台个人识别
个人级 persuasion score
操控建议
```

---

## 17. Phase 3 实现建议

### Phase 3A：本文件入库

```text
docs/research/evidence_to_opinion_ecosystem_mapping_v1.md
```

不改代码。

### Phase 3B：frontend-local mapping fixture

在前端或 mock data 里新增一个小型静态 Evidence fixture：

```text
mock EvidenceItem[]
→ local mapper
→ InfluenceCore / EchoBox / PeopleCluster / ResponseTempo
```

约束：

```text
不接 backend。
不接真实 API。
不 fetch URL。
不接 LLM。
只验证数据形状和 UI 映射。
```

### Phase 3C：backend schema-only

如果需要后端支持，先只做 schema / service stub：

```text
不接真实平台。
不调用外部网络。
不改现有 Evidence 行为。
使用 mock fixtures 做测试。
```

### Phase 3D：Evidence API read-only mapping

在现有 EvidenceItem 数据稳定后，再做：

```text
读取 case_evidence_items
→ local deterministic mapping
→ opinion ecosystem model objects
```

仍然不接真实 API。

---

## 18. 验证建议

### docs-only

```text
git status
```

### frontend-only

```text
npm --prefix frontend run build
```

### backend schema-only

```text
python -m pytest
python scripts\run_offline_benchmarks.py
```

不要因为 Phase 3 映射而：

```text
接真实平台 API
fetch URL
scrape 网站
接真实 LLM
集成 MediaCrawler / OpenClaw
重建 GitHub Actions CI
```

---

## 19. 后续 Source 更新建议

当前不要马上替换 Project Source。

当以下任一完成后，可以考虑更新 Source 08 或新增 Source 09：

```text
Evidence → Opinion Ecosystem Mapping 正式实现
Influence Core schema 正式实现
EchoBox schema 正式实现
People Cluster schema 正式实现
小球沙盒接入真实 EvidenceItem
真实 demo case 完成
Response Tempo 报告输出成型
```

当前阶段，本文件应放在 repo 的：

```text
docs/research/evidence_to_opinion_ecosystem_mapping_v1.md
```

而不是直接放入 ChatGPT Project Source。

---

## 20. 结论

Phase 3 的核心不是“接真实数据”，而是先让现有 Evidence Layer 能被稳定解释成舆论生态模型对象。

正确顺序是：

```text
先确定 EvidenceRole
再映射 SourceIdentity
再生成 Influence Core
再生成 EchoBox
再聚合 People Cluster
再计算 Camp Dynamics
再判断 Deconstruction / Response Tempo / Reputation Memory
```

这个顺序可以避免把人、内容、KOL、文章、视频、回音壁和小球混成一团。  
也能保证 Sentigraph 继续保持：

```text
合规证据治理
匿名人群建模
可解释权重
中观舆论结构分析
透明处理节奏建议
```

而不是滑向：

```text
全网爬虫
个人级操控
黑箱预测
虚假全量覆盖
```
