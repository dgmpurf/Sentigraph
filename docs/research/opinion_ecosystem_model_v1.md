# Sentigraph Opinion Ecosystem Model v1

**更新时间**：2026-06-13  
**用途**：沉淀 Sentigraph 下一阶段“舆论生态模型”的总体设计。本文是 research/design 文档，不代表当前代码已经实现。  
**建议存放位置**：`docs/research/opinion_ecosystem_model_v1.md`  
**相关文档**：

- `docs/research/sentigraph_ethical_public_opinion_simulation_research_report.md`
- `docs/research/github_public_opinion_systems_scan.md`
- `docs/research/opinion_ecosystem_weight_calculation_v1.md`
- `SENTIGRAPH_PROJECT_SOURCE_08_AGENT_BASED_SIMULATION_AND_WEIGHT_MODEL.md`

---

## 1. 一句话定位

Sentigraph 下一阶段的核心不是普通舆情 dashboard，而是：

> **事件舆论生态建模与处理节奏推演系统。**

它以合规证据为基础，将公开讨论中的观念核心、回音壁容器、人群小球、阵营迁移、二次解构、事件生命周期和长期声誉记忆组织成一个可解释的模拟系统，用于分析事件如何发酵、扩圈、降温、反噬或被重新解构。

它不是：

```text
全网自动爬虫
水军 / 带节奏 / 控评系统
个人级 persuasion optimizer
暗中影响、压制或骚扰公共讨论的工具
真实心理诊断系统
预测必然发生结果的黑箱模型
```

它应该是：

```text
证据治理系统
观念核心识别系统
回音壁容量与破圈风险分析系统
正 / 中 / 反人群权重分析系统
舆论生态沙盒模拟系统
处理节奏决策参考系统
```

---

## 2. 当前状态边界

本文不改变 Sentigraph 既有边界：

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

本文定义的是 Evidence 之上的下一阶段模型层，不表示这些层已经在代码中实现。

当前已完成：

```text
Evidence Layer
Trust / Dedup / Review / Audit
Evidence Scale / Coverage
Analysis / Report / Forecast / 当前聚合型 Simulation Lab
YouTube optional real-data path
CSV/Excel import
Manual URL Evidence
Vendor sample POC utilities
Source 08 小球沙盒与权重模型压缩记忆
research docs 入库
```

当前尚未正式实现：

```text
Influence Core / Narrative Core
EchoBox
People Cluster
Camp Dynamics
Deconstruction Core
Case Lifecycle
Response Tempo
Reputation Memory
Agent-Based 小球舆论生态沙盒
Evidence → Model 自动映射
真实历史事件 replay validation
```

---

## 3. 总体模型链路

后续建议把 Sentigraph 的舆论生态模型固定为：

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

解释：

```text
EvidenceItem：
证据材料，如视频、帖子、文章、评论、回复、CSV 行、Manual URL、vendor sample、YouTube raw data 等。

Influence Core / Narrative Core：
组织讨论的观念核心，例如 KOL 视频、媒体文章、爆火普通人内容、官方公告、反方论点、第三方说明、社区梗等。

EchoBox：
装着小球的框体，即回音壁 / 圈层边界 / 社区讨论容器。它有容量、渗透率、饱和度和破圈风险。

People Cluster：
小球。代表一小批相似人群或匿名参与者簇，而不是直接代表真实身份个人。

Camp Dynamics：
正 / 中 / 反阵营迁移规则，包括同化、中立化、退出、固化、反噬和潜伏再激活。

Deconstruction Core：
特殊的 Influence Core，用于表示梗化、符号重构、社区和解、叙事降压等二次解构机制。

Case Lifecycle：
事件生命周期阶段，如种子期、上升期、峰值期、疲劳期、衰退期、档案期、再激活期。

Response Tempo：
最终处理节奏建议，如澄清、FAQ、第三方说明、观察、低强度解构、避免回应、风险监测等。

Reputation Memory：
事件结束后留下的长期声誉残留，例如黑称、未解决不满、再激活触发器、信任恢复状态。
```

---

## 4. 核心原则

### 4.1 正方不是默认正确方

模型中不要把“正方”写死为“正确方”。推荐使用：

```text
focal_side：当前服务对象 / 客户方 / 主体方
support_side：支持 focal_side 的阵营
opposition_side：反对 focal_side 的阵营
neutral_side：中立 / 未定 / 围观阵营
```

原因：

```text
客户方在某些事件中可能确实有责任。
反对方核心论点可能含有事实依据。
中立者的判断可能取决于责任解释和证据补充。
系统不应服务于自我安慰，而应服务于真实风险判断。
```

### 4.2 小球是人群，不是 KOL / 文章 / 视频

```text
People Cluster / 小球：
一小批人、一类匿名参与者、一组相似观点人群。

Influence Core / 影响核心：
KOL 发声、视频、文章、帖子、媒体报道、官方公告、爆火普通人内容、梗化内容。

EchoBox / 框体：
回音壁容器、圈层边界、舆论生态箱。
```

KOL、主播、媒体、文章、视频不是普通小球。它们是观念核心或影响源，对小球产生吸附、排斥、中立化、极化、降温或解构作用。

### 4.3 猎食是视觉隐喻，不是消灭

内部视觉可以参考捕食者 / 猎物式生态模拟，但产品语义不应使用“消灭”“猎杀”。

模型语义应为：

```text
Assimilation / 同化：阵营迁移，颜色改变。
Neutralization / 中立化：强反对变弱反对或中立。
Disengagement / 退出：不再参与当前事件讨论。
Hardening / 固化：温和派变核心派，核心派更极端。
Backlash / 反噬：本来想降温，结果激怒中立或温和派。
Dormant Reactivation / 潜伏再激活：暂时退出的人群在未来类似事件中被重新唤起。
```

---

## 5. EvidenceItem：证据层

EvidenceItem 是所有上层模型的材料来源。当前 Sentigraph 已经有 Evidence Layer，因此后续模型应优先复用现有字段：

```text
platform
source_type
acquisition_mode
evidence_type
title
body_text
comment_text
parent_id
root_id
author_id
author_name
url
created_at
like_count
reply_count
share_count
view_count
provenance_type
verification_status
trust_score
trust_label
duplicate_group_id
duplicate_count
review_status
risk_flags
```

Evidence 层的职责：

```text
保留来源和证据链。
区分官方 API、用户上传、手动 URL、vendor sample、search candidate、mock fixture。
做 trust / dedup / review / audit。
避免低可信证据和重复证据直接放大声量。
```

所有上层权重都应受 Evidence Confidence 影响。

---

## 6. Influence Core / Narrative Core

### 6.1 定义

Influence Core 是舆论中的观念核心 / 影响核心。

它不是人，而是能组织、吸附、放大、解释、极化或解构人群观点的内容、论点、账号发声、文章、视频、公告或梗。

它可以是：

```text
KOL 视频
UP 主帖子
主播发声
新闻媒体报道
自媒体文章
论坛主帖
爆火普通人内容
官方公告
第三方解释
社区梗 / 二创 / 自嘲歌曲
反方核心论点
正方解释核心
中立分析核心
```

### 6.2 SourceIdentity 与 InfluenceCore 分离

必须区分：

```text
SourceIdentity = 谁发的
InfluenceCore = 发了什么
```

例如：

```text
某 UP 主本人：
source_identity，带有粉丝基础、受众立场、可信度、争议度。

某 UP 主发的视频：
influence_core，带有具体论点、证据、情绪、传播结果和评论区。
```

一个 SourceIdentity 可以发布多个 InfluenceCore。一个 InfluenceCore 也可能脱离原作者，变成社区自传播符号。

### 6.3 InfluenceCore 建议字段

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

  source_identity:
    source_id: string | null
    source_type:
      - kol
      - up
      - streamer
      - media
      - expert
      - official
      - organization
      - ordinary_user
      - community
      - unknown
    source_credibility: float
    audience_base_alignment:
      support: float
      neutral: float
      oppose: float
      unknown: float

  content_reference:
    title: string
    source_url: string | null
    platform: string
    aggregate_id: string | null
    evidence_ids: [string]
    created_at: datetime | null

  stance:
    stance_label: [support, neutral, oppose, mixed, unknown]
    stance_score: float
    stance_strength: float
    stance_confidence: float

  narrative:
    claim_summary: string
    frame_type: string
    evidence_strength: float
    logic_strength: float
    logical_vulnerability: float
    emotional_intensity: float
    extremity_score: float
    ambiguity_score: float

  attention:
    attention_weight: float
    growth_velocity: float
    ignition_score: float
    saturation_level: float
    decay_rate: float

  influence:
    gravitational_pull: float
    neutral_acceptance: float
    same_camp_reinforcement: float
    opponent_resistance: float
    bridge_power: float
    breakout_power: float
    deconstruction_potential: float

  risk:
    escalation_risk: float
    polarization_risk: float
    misinformation_risk: float
    backlash_risk: float
    response_priority: float

  confidence:
    evidence_confidence: float
    low_trust_share: float
    reviewed_share: float
    parameter_source:
      - observed_from_data
      - inferred_proxy
      - assumption_driven
      - manual_parameter
      - mock_default
      - low_confidence
```

### 6.4 何时生成 Influence Core

不是所有评论都能成为核心。第一版建议满足以下条件之一或多个时生成候选核心：

```text
高传播：播放、阅读、点赞、评论、转发、引用达到阈值。
高增长：短时间内快速增加讨论。
高引用：被多个评论区、帖子、视频、文章反复引用。
高阵营聚集：某个阵营明显围绕它形成共识。
高桥接：把事件带出原圈层。
高导火索：事件爆发或二次升级起点。
高权威：官方、媒体、专家、核心当事方发布。
高争议：同时吸引正反双方围攻或辩论。
高解构潜力：有明显梗化、二创、符号重构可能。
```

---

## 7. Narrative Logic：叙事逻辑结构

Influence Core 不只是正 / 反 / 中，它还应该有逻辑结构。

建议字段：

```yaml
NarrativeLogic:
  claim: string
  evidence_used: [string]
  causal_story: string
  moral_frame: string
  strongest_point: string
  weakest_point: string
  common_counterargument: string
  logic_strength: float
  evidence_strength: float
  emotional_substitution_risk: float
```

作用：

```text
识别反方核心是否有事实依据。
识别官方回应是否避开了关键逻辑缺口。
识别中立者为什么被某个论点吸引。
识别什么时候应该先补证据，而不是直接解构。
```

---

## 8. EchoBox：回音壁容器

### 8.1 定义

EchoBox 是装着小球的框体。它代表某个事件当前所在的回音壁 / 圈层边界 / 舆论生态箱。

一个 EchoBox 可以对应：

```text
一个 UP 视频评论区
一个贴吧楼
一个微博话题下的阵营讨论区
一个游戏社区论坛串
一个粉丝圈层
一个路人讨论区
一个媒体报道外圈
```

### 8.2 EchoBox 的核心概念

```text
carrying_capacity：容量上限。这个圈层最多能触达或容纳多少关注/参与。
permeability_score：渗透率。外部路人进入难度。
saturation_ratio：饱和度。当前活跃度 / 容量上限。
internal_reinforcement：内部强化。是否在互相重复、互相增强。
breakout_risk：破圈风险。是否可能从圈内高热扩展到圈外。
external_inflow_rate：新路人进入速度。
fatigue_rate：圈内疲劳速度。
```

### 8.3 EchoBox 建议字段

```yaml
EchoBox:
  box_id: string
  case_id: string
  platform: string
  box_type:
    - aggregate_box
    - community_box
    - creator_audience_box
    - topic_box
    - cross_platform_box
    - media_outer_box
    - unknown

  aggregate_ids: [string]
  influence_core_ids: [string]
  people_cluster_ids: [string]
  source_url_ids: [string]

  boundary:
    echo_chamber_score: float
    permeability_score: float
    breakout_risk: float
    carrying_capacity: float
    saturation_ratio: float

  dynamics:
    internal_reinforcement: float
    external_inflow_rate: float
    fatigue_rate: float
    growth_velocity: float
    decay_rate: float

  external_triggers:
    kol_entry_risk: float
    media_entry_risk: float
    platform_boost_risk: float
    new_evidence_risk: float
    official_response_risk: float

  visual:
    box_size: float
    border_strength: float
    border_openness: float
    density: float
    dominant_color: string
    warning_state: string
```

### 8.4 EchoBox 的判断意义

```text
高热 + 低渗透：圈内爆炸，圈外无感。
中热 + 高渗透：现在不大，但容易扩圈。
高饱和 + 高疲劳：可能自然衰减。
高破圈 + 外部触发：需要预警。
```

---

## 9. People Cluster：人群小球

### 9.1 定义

People Cluster 是沙盒里的小球。它代表一小批相似人群或匿名参与者簇，而不是直接代表真实身份个人。

它可以表示：

```text
正方核心人群
温和支持者
中立围观者
中立参与者
温和反对者
反方核心人群
极端反对者
疲劳退出者
潜伏不满者
```

### 9.2 People Cluster 建议字段

```yaml
PeopleCluster:
  cluster_id: string
  case_id: string
  echo_box_id: string
  source_actor_ids: [string]
  evidence_ids: [string]

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

  stance_score: float
  stance_strength: float
  mobility: float
  identity_lock: float
  evidence_sensitivity: float
  emotion_load: float
  fatigue: float
  grievance_memory: float
  deconstruction_receptivity: float
  social_cost_to_switch: float

  trust_profile:
    official: float
    media: float
    expert: float
    kol: float
    peer: float
    community_core: float

  face_saving:
    public_commitment_level: float
    face_saving_need: float
    switch_cost: float
    ridicule_risk_if_switch: float

  current_attention: float
  last_trigger_id: string | null

  visual:
    color: string
    size: float
    speed: float
    opacity: float
    glow: float
    border_style: string
```

### 9.3 People Cluster 的重要注意事项

```text
mobility 高：容易从中立变支持/反对，或从温和反对转中立。
identity_lock 高：核心派，不容易变色。
evidence_sensitivity 高：更吃证据、逻辑、第三方说明。
emotion_load 高：更容易被极端核心吸附，也更容易反噬。
fatigue 高：可能退出讨论或接受解构。
grievance_memory 高：即使退出，也容易未来重新激活。
```

这些都是公开行为代理指标，不是系统真的知道个人心理。

---

## 10. Camp Dynamics：阵营动力学

### 10.1 定义

Camp Dynamics 描述正 / 中 / 反人群小球如何在 Influence Core、EchoBox、事件冲击和处理节奏影响下发生迁移、强化、中立化、退出、反噬和解构。

### 10.2 阵营状态

底层状态：

```text
support_core
support_soft
neutral_observing
neutral_engaged
oppose_soft
oppose_core
oppose_extreme
withdrawn
dormant_grievance
```

公开 UI 可以简化为：

```text
支持 / 中立 / 反对 / 退出 / 潜伏风险
```

### 10.3 六种基本转移

#### 同化 Assimilation

```text
neutral_engaged → support_soft
oppose_soft → neutral_engaged → support_soft
support_soft → neutral_engaged → oppose_soft
```

核心派通常不直接同化。

#### 中立化 Neutralization

```text
oppose_soft → neutral_engaged
oppose_soft → neutral_observing
support_soft → neutral_observing
```

很多情况下，中立化比让对方支持更现实。

#### 退出 Withdrawal

```text
小球透明度下降，速度变慢，从 EchoBox 淡出。
```

退出不等于和解，需要记录 grievance_memory。

#### 固化 / 极化 Hardening

```text
oppose_soft → oppose_core
oppose_core → oppose_extreme
support_soft → support_core
```

#### 反噬 Backlash

```text
neutral_observing → oppose_soft
support_soft → neutral_engaged → oppose_soft
withdrawn → dormant_grievance → oppose_soft
```

#### 潜伏再激活 Dormant Reactivation

```text
withdrawn + high grievance_memory → dormant_grievance
dormant_grievance + new shock → oppose_soft / oppose_core
```

---

## 11. Deconstruction Core：二次解构核心

### 11.1 定义

Deconstruction Core 是 Influence Core 的特殊类型。

它表示把原本高冲突、高敌意、高威胁的事件叙事，转化为低威胁、可消费、可自嘲、可共存符号的影响核心。

它不是“洗白”，而是：

```text
叙事降压
符号重构
社区和解
误解消解
攻击性降低
事件语义转移
```

### 11.2 例子类型

```text
自嘲歌曲
梗图
二创视频
社区口号
反讽式回应
轻量解释视频
第三方调侃
当事人参与再创作
粉丝/路人共同使用的新符号
```

### 11.3 DeconstructionCore 建议字段

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
    - archive_summary
    - neutral_explainer
    - unknown

  timing:
    timing_window:
      - early
      - middle
      - late
      - post_peak
    peak_distance: float
    fatigue_context: float

  prerequisites:
    factual_clarity_required: bool
    apology_required: bool
    remedy_required: bool
    community_readiness_required: bool

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

  target_groups:
    support_core: float
    support_soft: float
    neutral_observing: float
    neutral_engaged: float
    oppose_soft: float
    oppose_core: float
    oppose_extreme: float

  output:
    deconstruction_fit_score: float
    recommended_window: string
    warning_notes: [string]
```

### 11.4 解构适用条件

适合影响：

```text
中立参与者
温和反对者
疲劳中的围观者
对事实已有基本理解但仍情绪不满的人
```

不适合直接影响：

```text
反方极端派
受害叙事强绑定者
责任未处理清楚的事件
仍处于事实争议峰值的事件
```

---

## 12. Case Severity：事件严重度闸门

在输出任何处理节奏前，必须先判断事件严重度与责任结构。

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
严重伤害高、事实不清、责任未处理时，不建议解构。
如果真实补救未完成，不要直接建议梗化或自嘲。
如果事件涉及高敏内容，应输出谨慎或禁止建议。
```

---

## 13. Case Lifecycle：事件生命周期

事件所处阶段会影响所有处理节奏。

```yaml
CaseLifecycle:
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
    current_level: float
    growth_velocity: float
    decay_rate: float
    volatility: float
  peak_distance: float
  reactivation_signal: float
```

阶段解释：

```text
seed：种子期，少数人开始讨论。
rise：上升期，讨论扩散。
peak：峰值期，阵营强冲突。
plateau：高位平台期，持续争论。
fatigue：疲劳期，新增参与下降。
decay：衰退期，声量下降。
archive：档案期，变成长期标签或梗。
reactive：再激活期，被新事件重新点燃。
```

处理逻辑：

```text
上升期：重点解释事实，防止错误叙事定型。
峰值期：重点止血，避免高压和情绪对撞。
疲劳期：可考虑降压、第三方解释、低强度解构。
档案期：关注长期污名和未来再激活。
```

---

## 14. Response Tempo：处理节奏

Response Tempo 是最终输出，不是具体执行操控。

它应该回答：

```text
现在是否需要回应？
回应是澄清、FAQ、长文、视频说明、第三方说明，还是先观察？
是否已经进入解构窗口？
是否应该避免玩梗？
哪个 EchoBox 破圈风险最高？
哪个 Influence Core 是当前核心矛盾？
哪些人群只是退出，不代表理解？
```

建议字段：

```yaml
ResponseTempo:
  case_id: string
  recommended_mode:
    - clarify_now
    - faq_or_explainer
    - third_party_explanation
    - monitor_only
    - prepare_low_intensity_deconstruction
    - observe_organic_memes
    - avoid_deconstruction
    - high_risk_do_not_escalate

  priorities:
    clarification_priority: float
    faq_priority: float
    third_party_explanation_priority: float
    deconstruction_window_score: float
    wait_and_monitor_score: float
    backlash_risk: float

  recommended_sequence:
    - step: string
      reason: string
      risk: string
      uncertainty: string

  warnings:
    - string

  coverage_note: string
  uncertainty_note: string
```

示例输出：

```text
当前事件仍处于上升期，反方核心论点尚未被事实层解释覆盖。
不建议立即解构或玩梗。
建议先发布事实时间线和 FAQ，重点覆盖中立参与者与温和反对者。
当前 EchoBox 破圈风险中等，但外圈主播介入会显著提高风险。
```

---

## 15. Reputation Memory：长期声誉记忆

事件结束不代表影响清零。

建议对象：

```yaml
ReputationMemory:
  case_id: string
  subject_id: string
  stigma_tags: [string]
  unresolved_grievance_score: float
  meme_persistence: float
  trust_recovery: float
  dormant_grievance_share: float
  reactivation_triggers: [string]
  next_event_sensitivity: float
  monitoring_recommendation: string
```

它用来判断：

```text
事件是否留下长期黑称？
是否只是声量下降而不是真正解决？
下次类似事件是否容易被重新激活？
某个梗是降压了，还是固化了污名？
```

---

## 16. Counterfactual Baseline：反事实基线

每个 Response Tempo 必须比较至少一个基线。

建议场景：

```text
no_response_baseline：什么都不做。
minimal_response：最低限度回应。
clarification：事实澄清。
faq_or_explainer：FAQ / 长文 / 视频说明。
third_party_explanation：第三方说明。
deconstruction：低强度解构。
late_response：延迟回应。
wrong_tone_response：语气错误回应。
```

原因：

```text
如果方案 A 后风险下降 10%，但什么都不做也会下降 12%，方案 A 可能没有价值。
如果解构短期降温但长期 stigma 上升，不能只看短期曲线。
```

---

## 17. Failure Mode：失败模式

系统必须输出方案可能如何失败。

```yaml
FailureMode:
  assumption: string
  failure_condition: string
  possible_backlash: string
  monitoring_signal: string
  mitigation: string
```

示例：

```text
假设：中立者主要缺少事实信息。
失败条件：中立者其实已经不信任官方来源。
可能反噬：官方公告被解读为狡辩。
监控信号：公告下方“避重就轻”评论快速上升。
缓解：改用第三方解释或补充原始证据。
```

---

## 18. 不确定性与参数来源

每个权重和结论必须标注来源：

```text
observed_from_data：数据直接观察。
inferred_proxy：公开行为代理推断。
assumption_driven：模型假设。
manual_parameter：人工设定。
mock_default：demo 默认值。
low_confidence：低置信。
```

必须避免：

```text
把真实私下立场说成已知。
把沉默者态度说成已知。
把因果影响说成确定。
把低可信证据当成事实。
把 mock 模拟说成真实预测。
```

输出中必须带：

```text
当前结果基于已导入 / 可用证据和模型假设，不代表全网全量覆盖，也不代表因果确定。
```

---

## 19. Opinion Ecosystem Sandbox：舆论生态沙盒

### 19.1 视觉语义

```text
框体 = EchoBox / 回音壁容器
小球 = People Cluster / 人群簇
发光核心 = Influence Core / 观念核心
特殊核心 = Deconstruction Core / 解构核心
边界厚度 = 回音壁强度
边界缺口 = 渗透率
框体扩大 = 破圈 / 扩圈
新框体出现 = 新圈层进入
小球变色 = 阵营迁移
小球变透明 = 退出讨论
暗色残影 = 潜伏反噬风险
```

### 19.2 小球状态变化

```text
红 → 灰：反对中立化。
灰 → 绿：中立向 focal_side 支持迁移。
绿 → 灰 / 红：基本盘流失或反方吸附。
红 / 绿 → 透明：退出当前事件讨论。
透明 + 暗影：退出但残余不满仍在。
```

### 19.3 扩圈变量

```text
外圈 KOL 介入
大主播下场
媒体报道
官方回应
新证据
二次爆料
平台推荐
跨平台搬运
高桥接节点转发
```

这些变量会改变：

```text
EchoBox 容量
渗透率
破圈风险
外部路人进入速度
People Cluster 分布
Influence Core 权重
```

---

## 20. C 端与 B 端输出差异

### C 端公开展示

```text
事件摘要
正 / 中 / 反趋势
公开小球沙盒
回音壁是否破圈
核心争议点摘要
覆盖与不确定性提示
用户投票 / 请求分析
```

C 端默认显示 People Cluster，不显示单个匿名 actor。

### B 端专业报告

```text
私有 case
证据来源和可信度
Influence Core 排行
EchoBox 容量和破圈风险
People Cluster 权重
Camp Dynamics 转移趋势
Deconstruction Window
Response Tempo
Failure Mode
Reputation Memory
```

B 端可以 drill down 到匿名 actor，但仍不展示原始 uid / 用户名，不做跨平台真实身份对齐。

---

## 21. MVP 实现路线

### Phase 0：文档沉淀

```text
Source 08 已加入 Project Source。
完整 research report 放入 docs/research/。
GitHub 参考项目扫描放入 docs/research/。
Weight Calculation v1 放入 docs/research/。
本文件 Opinion Ecosystem Model v1 放入 docs/research/。
```

### Phase 1：mock 沙盒视觉原型

```text
前端 only。
不接真实数据。
不调用 API。
不接 LLM。
100–300 个小球。
1–3 个 EchoBox。
若干 Influence Core。
支持播放 / 暂停 / 重置 / 场景切换。
```

### Phase 2：schema-only mock 权重

```text
定义 InfluenceCore schema。
定义 EchoBox schema。
定义 PeopleCluster schema。
定义 CampDynamics output schema。
定义 ResponseTempo output schema。
全部使用 mock fixtures。
```

### Phase 3：Evidence → Model 映射

```text
EvidenceItem → Influence Core candidate
EvidenceItem → People Cluster / Anonymous Actor
source_url / platform / aggregate → EchoBox
comment_text / body_text → stance / sentiment / topic
like/reply/share/view → attention / influence proxy
trust/dedup/review → confidence weighting
```

### Phase 4：真实 demo 数据

```text
真实事件 + 合规导入证据。
优先使用 CSV/Excel、Manual URL、可选 YouTube official API。
不硬接抖音/B站/小红书 live API。
明确 coverage note。
```

### Phase 5：B 端报告 + C 端公开页

```text
C 端：公开事件推演页和小球沙盒。
B 端：专业报告、权重、热区、处理节奏、风险模式。
```

---

## 22. 暂不建议实现的内容

不要在第一版做：

```text
真实抖音/B站/小红书 API adapter
真实 RSS/GDELT/Search provider
真实 vendor adapter
真实 LLM social simulation
MediaCrawler integration
OpenClaw production ingestion
个人级 persuasion ranking
水军 / bot / sockpuppet 模拟
跨平台个人身份识别
真实心理诊断
自动判断某人是水军或串子
```

---

## 23. 与 Weight Calculation v1 的关系

本文件负责解释：

```text
整个舆论生态模型是什么。
对象之间如何组织。
小球、核心、框体、生命周期、处理节奏分别代表什么。
```

`opinion_ecosystem_weight_calculation_v1.md` 负责解释：

```text
各类权重如何计算。
Evidence Confidence 怎么影响后续分数。
Influence Core / EchoBox / People Cluster / Camp Dynamics / Response Tempo 的分数如何形成。
```

两者关系：

```text
Opinion Ecosystem Model v1 = 总体世界观与对象模型。
Weight Calculation v1 = 计算规则和分数骨架。
```

---

## 24. 后续 Source 更新建议

暂时不要把本文直接放进 ChatGPT Project Source。

建议先放入 repo：

```text
docs/research/opinion_ecosystem_model_v1.md
```

当以下条件之一发生时，再考虑生成 Source 09 或替换 Source 08：

```text
Influence Core schema 正式实现。
EchoBox schema 正式实现。
People Cluster schema 正式实现。
Agent-Based 小球沙盒上线。
Evidence → Model 映射上线。
真实事件 demo 完成。
Simulation Lab 从聚合预演升级为 Opinion Ecosystem Sandbox。
```

---

## 25. 结论

Sentigraph 的下一阶段不应只是“更多舆情功能”，而应转向：

```text
事件舆论生态建模
观念核心识别
回音壁容量与破圈风险
人群小球阵营迁移
二次解构窗口判断
处理节奏建议
长期声誉记忆
```

这套模型可以支撑：

```text
C 端公开事件推演平台
B 端专业舆情 / 公关 / MCN / 艺人 / 品牌服务
```

第一步仍应保持克制：先做 mock 沙盒和 schema，不接真实平台 API、不接真实 LLM、不改变合规边界。
