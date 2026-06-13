# Sentigraph Evidence → Opinion Ecosystem Mapping Contract v1

**建议存放路径**：`docs/research/evidence_to_opinion_ecosystem_mapping_contract_v1.md`  
**文档性质**：research/design handoff document  
**当前状态**：前端本地 mock / synthetic fixture / deterministic mapper 阶段  
**重要说明**：本文件不是 Project Source，不代表后端 API、真实 Evidence 映射、真实平台数据、真实 LLM 或真实 agent simulation 已实现。

---

## 1. Purpose / 用途

本文件用于把当前前端本地 mock mapper 的设计沉淀成一份 **Evidence → Opinion Ecosystem Mapping Contract**，方便后续把现有 Evidence Layer 安全、可解释地接入舆论生态模型。

当前已经有：

```text
Phase 1: frontend-only mock visual sandbox
Phase 2: frontend-local mock schema / mock weight model
Phase 3A: Evidence → Opinion Ecosystem mapping design note
Phase 3B: synthetic EvidenceItem fixture + deterministic local mapper
Phase 3C: local mapper contract validator
```

本文件是 **Phase 3D**：

```text
Phase 3D: mapping contract / backend handoff design
```

它回答：

```text
EvidenceItem 需要哪些字段？
哪些 EvidenceItem 可以成为 InfluenceCore？
哪些 EvidenceItem 只能作为评论 / 人群信号？
source_url / root_id / platform 怎么进入 EchoBox？
author_id / author_name 怎么变成匿名 PeopleCluster？
trust / review / dedup 怎么影响权重？
rejected / duplicate / low-trust 证据如何处理？
前端 mock mapper 与未来 backend mapper 的边界是什么？
```

---

## 2. Boundary / 边界

本文件不改变 Sentigraph 当前项目边界。

仍然必须保留：

```text
Sentigraph 不是全网自动爬虫。
当前真实官方 API 路径只有可选本地 YouTube。
Douyin / Bilibili / Xiaohongshu / Reddit / Weibo 等真实接入仍 pending。
Search Discovery / RSS / GDELT 当前是 mock/static，不是 live provider。
Vendor POC 是离线样本映射，不是真实 vendor adapter。
Vendor data 默认 vendor_attested / medium_low，不是 official verified。
LLM provider 仍为 mock。
MediaCrawler 不集成主线。
OpenClaw / 龙虾只能作为外部人工辅助工具，不是 production ingestion。
Evidence Scale / Coverage 不代表全网全量覆盖。
Opinion Ecosystem Sandbox 当前仍是 mock / prototype，不代表真实数据驱动 simulation 已完成。
```

---

## 3. Current frontend prototype status / 当前前端原型状态

当前前端已有本地 mock 链路：

```text
synthetic EvidenceItem fixture
→ deterministic local mapper
→ local contract validator
→ Opinion Ecosystem Sandbox UI
```

相关前端文件：

```text
frontend/src/data/opinionEcosystemEvidenceFixture.js
frontend/src/data/opinionEcosystemMapper.js
frontend/src/data/opinionEcosystemValidator.js
frontend/src/data/opinionEcosystemMock.js
frontend/src/pages/OpinionEcosystemSandbox.jsx
```

当前这些文件只允许使用：

```text
local synthetic fixture
local deterministic helper
local UI rendering
local validation
```

不得使用：

```text
backend API
real Evidence data
real platform data
real LLM
URL fetch
scraping
MediaCrawler
OpenClaw production ingestion
```

---

## 4. Canonical model chain / 标准模型链路

后续 Mapping Contract 应围绕这条链路设计：

```text
EvidenceItem
→ EvidenceRole
→ SourceIdentity
→ InfluenceCore / NarrativeCore
→ EchoBox
→ PeopleCluster
→ CampDynamics
→ DeconstructionCore
→ CaseLifecycle
→ ResponseTempo
→ ReputationMemory
```

解释：

```text
EvidenceItem:
  原始证据单位。可以是视频、帖子、文章、评论、回复、官方公告、第三方解释、梗化内容等。

EvidenceRole:
  证据在舆论生态模型中的角色分类。

SourceIdentity:
  发布者或来源身份。可以是 KOL / UP / 媒体 / 官方 / 普通用户 / 社区来源，但不得直接暴露原始身份。

InfluenceCore / NarrativeCore:
  观念核心。KOL 视频、媒体文章、官方公告、爆火普通人内容、反方核心视频、第三方解释、梗化内容等都可以成为 InfluenceCore。
  InfluenceCore 不是小球，也不是 PeopleCluster。

EchoBox:
  回音壁容器。表示某个事件讨论被困住或扩散的圈层 / 社区 / 内容容器。

PeopleCluster:
  人群小球。代表一小批匿名参与者 / 相似观点群体，不代表真实个人。

CampDynamics:
  同化、中立化、退出、固化、反噬、潜伏再激活的状态转移倾向。

DeconstructionCore:
  解构核心。表示梗化、符号重构、叙事降压、社区和解等特殊 InfluenceCore。

CaseLifecycle:
  事件生命周期。seed / rise / peak / plateau / fatigue / decay / archive / reactive。

ResponseTempo:
  处理节奏建议。澄清、FAQ、第三方解释、观察、解构窗口等。

ReputationMemory:
  长期声誉残留。未解决不满、黑称固化、梗持续、未来再激活风险等。
```

---

## 5. EvidenceItem input contract / EvidenceItem 输入契约

### 5.1 Required fields / 必需字段

未来正式 mapper 至少应要求：

```yaml
EvidenceItem:
  evidence_id: string
  case_id: string
  platform: string
  evidence_type: string
  acquisition_mode: string
  provenance_type: string
  verification_status: string
  trust_label: string
  review_status: string
```

如果这些字段缺失：

```text
evidence_id 缺失 → 不可映射，应生成 validation failure。
case_id 缺失 → 不可映射，应生成 validation failure。
platform 缺失 → 映射到 unknown_platform，并降低 confidence。
evidence_type 缺失 → 映射到 unknown evidence role，并降低 confidence。
trust / provenance / verification / review 字段缺失 → 进入 low_confidence / needs_review 处理。
```

### 5.2 Recommended fields / 推荐字段

```yaml
EvidenceItem:
  title: string | null
  body_text: string | null
  comment_text: string | null
  url: string | null
  source_url: string | null
  root_id: string | null
  parent_id: string | null
  author_id: string | null
  author_name: string | null
  created_at: datetime | null
  like_count: number | null
  reply_count: number | null
  share_count: number | null
  view_count: number | null
  favorite_count: number | null
  repost_count: number | null
  content_hash: string | null
  duplicate_group_id: string | null
  duplicate_count: number | null
  risk_flags: [string]
```

这些字段用于：

```text
title / body_text / comment_text → stance / topic / narrative / emotion proxy
url / source_url / root_id / parent_id → root content / EchoBox / InfluenceCore grouping
author_id / author_name → anonymous actor / PeopleCluster grouping
created_at → lifecycle / growth / fatigue / decay
like / reply / share / view → attention / engagement / influence proxy
content_hash / duplicate_group_id → dedup / anti-amplification
risk_flags → warning / trust penalty / review queue
```

---

## 6. EvidenceRole classification / 证据角色分类

Mapper 应先为每条 EvidenceItem 生成一个 `EvidenceRole`。

建议角色：

```yaml
EvidenceRole:
  role:
    - influence_core_candidate
    - deconstruction_core_candidate
    - official_response_candidate
    - third_party_explanation_candidate
    - source_identity_signal
    - people_cluster_signal
    - echo_box_signal
    - supporting_context
    - low_trust_warning
    - rejected_excluded
    - unknown
```

### 6.1 InfluenceCore candidate

满足任一条件可成为候选：

```text
evidence_type in [video, post, article, official_statement, third_party_explanation, meme, forum_thread]
或 root_id 为空且有大量 child comments
或 source_type / provenance 指向 official / media / expert / KOL / organization
或被多个评论 / 回复 / 其他 Evidence 引用
或是事件导火索 / 二次升级 / 高传播内容
```

注意：

```text
普通评论默认不成为 InfluenceCore。
普通人发布的内容如果爆火、被引用、成为导火索，可以成为 viral_ordinary_content InfluenceCore。
```

### 6.2 PeopleCluster signal

满足条件：

```text
evidence_type in [comment, reply]
或包含 comment_text
或有 parent_id 指向某个 root content
```

它用于生成人群簇信号，不直接变成小球个人。

### 6.3 DeconstructionCore candidate

满足条件：

```text
evidence_type == meme
或 body_text / title / tags 显示梗化、二创、自嘲、社区口号、仪式化短语
或被标记为 community_deconstruction / symbolic_reframe / parody / music_video / meme_reframe
```

注意：

```text
DeconstructionCore 是 InfluenceCore 的特殊类型。
它用于叙事降压 / 符号重构 / 社区和解判断。
它不是“洗白”模块。
```

### 6.4 Rejected excluded

```text
review_status == rejected
或 verification_status in [rejected, human_rejected]
```

处理：

```text
不进入 active weights。
可以进入 validation statistics / audit warning。
不得放大热度、人群数、阵营比例或 ResponseTempo。
```

---

## 7. Evidence gating / 证据门控规则

### 7.1 Rejected evidence

```text
rejected evidence active_weight = 0
不参与：
  InfluenceCore attention
  PeopleCluster population
  EchoBox saturation
  CampDynamics transition
  ResponseTempo recommendation
```

可以参与：

```text
audit count
rejected evidence note
validator check
```

### 7.2 Low-trust evidence

```text
trust_label in [low, unverified]
或 review_status in [review_needed, needs_more_source, marked_weak]
或 verification_status in [needs_review, user_attested_unverified, vendor_attested]
```

处理：

```text
可以参与映射，但必须降权。
必须标记 confidence 较低。
如果低信任占比高，ResponseTempo 必须提示证据不足 / 需复核。
```

### 7.3 Duplicate evidence

```text
同一 duplicate_group_id 下的多条 EvidenceItem 不得作为多名独立参与者重复计算。
```

推荐：

```text
unique_evidence_count 用于主计数。
duplicate_count 作为重复信号。
duplicate_group_id 可提高 repetition_score，但不能放大真实参与人数。
```

### 7.4 Mock fixture evidence

```text
acquisition_mode == mock_fixture
provenance_type == mock_fixture
verification_status == mock_fixture
```

处理：

```text
可以驱动 demo。
必须显示 mock / static / synthetic label。
不得被 UI 或报告说成真实 Evidence。
```

---

## 8. SourceIdentity contract / 来源身份契约

`SourceIdentity` 用于区分：

```text
谁发的
和
发了什么
```

两者不能混淆。

```yaml
SourceIdentity:
  source_id: string
  case_id: string
  platform: string
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
  source_credibility: number
  audience_base_alignment:
    support: number
    neutral: number
    oppose: number
    unknown: number
  raw_identity_hidden: true
  confidence: number
```

要求：

```text
SourceIdentity 可以关联多个 InfluenceCore。
InfluenceCore 必须指向它承载的具体内容 / 论点。
KOL / 媒体 / 官方不是 PeopleCluster 小球。
SourceIdentity 不得暴露原始 uid / username / real-world identifier。
```

---

## 9. InfluenceCore mapping contract / InfluenceCore 映射契约

### 9.1 Required output fields

```yaml
InfluenceCore:
  core_id: string
  core_type: string
  label: string
  stance_label: string
  stance_score: number
  source_type: string
  source_credibility: number
  evidence_strength: number
  logic_strength: number
  emotional_intensity: number
  extremity_score: number
  gravitational_pull: number
  neutral_acceptance: number
  same_camp_reinforcement: number
  opponent_resistance: number
  bridge_power: number
  breakout_power: number
  deconstruction_potential: number
  backlash_risk: number
  confidence: number
  parameter_source: string
```

### 9.2 Mapping rules

```text
official_statement → official_statement InfluenceCore
third_party_explanation → third_party_explanation InfluenceCore
meme / parody / self_mockery → DeconstructionCore candidate
video / post / article / forum_thread → creator_video / creator_post / media_article / forum_thread InfluenceCore
ordinary root content with high engagement / high references → viral_ordinary_content InfluenceCore
```

### 9.3 Object separation rule

```text
InfluenceCore 不得渲染为 PeopleCluster 小球。
InfluenceCore 应渲染为 core node / attractor / resource / narrative core。
InfluenceCore 的颜色可以表示 stance，但它不是人群。
```

---

## 10. EchoBox mapping contract / EchoBox 映射契约

EchoBox 表示回音壁容器 / 圈层边界 / 讨论容量。

```yaml
EchoBox:
  box_id: string
  case_id: string
  label: string
  platform: string
  box_type: string
  aggregate_ids: [string]
  influence_core_ids: [string]
  people_cluster_ids: [string]
  echo_chamber_score: number
  carrying_capacity: number
  saturation_ratio: number
  permeability_score: number
  internal_reinforcement: number
  external_inflow_rate: number
  fatigue_rate: number
  breakout_risk: number
  lifecycle_stage: string
  confidence: number
  parameter_source: string
```

Mapping grouping priority:

```text
1. platform + root_id
2. platform + source_url canonical group
3. platform + influence_core_id
4. platform + topic-like grouping
5. unknown_echo_box fallback
```

重要：

```text
EchoBox 不是普通 UI 框体。
它代表事件目前被困住或扩散的讨论容器。
EchoBox 有容量、饱和度、渗透率、破圈风险。
```

---

## 11. PeopleCluster mapping contract / PeopleCluster 映射契约

PeopleCluster 表示小球人群簇。

```yaml
PeopleCluster:
  cluster_id: string
  label: string
  camp_state: string
  stance_label: string
  stance_score: number
  stance_strength: number
  population_weight: number
  mobility: number
  identity_lock: number
  evidence_sensitivity: number
  emotion_load: number
  fatigue: number
  grievance_memory: number
  deconstruction_receptivity: number
  social_cost_to_switch: number
  influence_weight: number
  activity_weight: number
  expression_intensity: number
  confidence: number
  parameter_source: string
```

Rules:

```text
小球代表人群簇，不代表真实个人。
不得暴露 author_id / author_name。
author_id / author_name 只能用于本地匿名聚合和 cluster grouping。
默认不做跨平台同一人识别。
如果只有 author_name，没有 author_id，则 confidence 降低。
如果没有任何 author signal，则进入 anonymous_unknown bucket。
```

Camp states:

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

---

## 12. CampDynamics contract / 阵营动力学契约

```yaml
CampDynamics:
  conversion_score: number
  neutralization_score: number
  withdrawal_score: number
  hardening_score: number
  backlash_score: number
  reactivation_risk: number
```

Meaning:

```text
conversion_score:
  同化 / 阵营迁移可能。

neutralization_score:
  温和反对 / 中立参与者转为观望或低冲突的可能。

withdrawal_score:
  退出当前事件讨论的可能。

hardening_score:
  温和派变核心派、核心派极化的可能。

backlash_score:
  回应、解构或错误时机造成反噬的风险。

reactivation_risk:
  退出后未来被新事件重新激活的风险。
```

---

## 13. DeconstructionCore contract / 解构核心契约

```yaml
DeconstructionCore:
  core_id: string
  label: string
  deconstruction_type: string
  target_core_id: string | null
  threat_deflation: number
  humor_acceptance: number
  face_saving_score: number
  neutralization_power: number
  conversion_power: number
  withdrawal_power: number
  ridicule_persistence: number
  meme_replicability: number
  community_co_creation: number
  backlash_risk: number
  long_term_stigma_risk: number
  deconstruction_fit_score: number
```

Rules:

```text
解构不是洗白。
解构是叙事降压、符号重构、社区和解、误解消解。
事实不清、责任未处理、真实伤害高时，不应推荐强行解构。
解构可能降低冲突，也可能固化黑称或引发反噬。
```

---

## 14. ResponseTempo contract / 处理节奏契约

```yaml
ResponseTempo:
  clarification_priority: number
  faq_priority: number
  third_party_explanation_priority: number
  deconstruction_window_score: number
  wait_and_monitor_score: number
  recommendation_label: string
  recommendation_text: string
  risk_notes: [string]
```

Allowed recommendation types:

```text
补充事实说明
FAQ / 长文解释
第三方说明
等待观察
谨慎低强度解构
暂不建议解构
反噬预警
基本盘防流失
破圈风险预警
```

Disallowed product-facing language:

```text
水军
控评
带节奏
压制
猎杀
洗白
操控
精准影响用户
最易被说服的人
```

---

## 15. ReputationMemory contract / 长期声誉残留契约

```yaml
ReputationMemory:
  unresolved_grievance_score: number
  stigma_persistence: number
  meme_persistence: number
  trust_recovery: number
  reactivation_risk: number
  monitoring_notes: [string]
```

Meaning:

```text
公开声量下降不等于问题解决。
退出讨论不等于理解或和解。
梗化可能短期降压，也可能长期固化黑称。
相似事件可能重新激活 dormant grievance。
```

---

## 16. Weight and confidence normalization / 权重与置信度规范

所有 weight-like fields 必须满足：

```text
0.0 <= value <= 1.0
```

所有模型对象建议携带：

```yaml
confidence: number
parameter_source:
  - observed_from_data
  - inferred_proxy
  - assumption_driven
  - manual_parameter
  - mock_default
  - low_confidence
```

不能把以下内容说成可直接知道：

```text
真实私下立场
个人真实心理
沉默者真实态度
个体级可说服性
真实因果影响
跨平台同一人身份
```

---

## 17. Future backend handoff / 未来后端交接建议

本节仅为未来建议，不代表当前要实现。

### 17.1 Future service boundary

未来正式接入时，建议后端提供一个独立 service：

```text
backend/services/opinion_ecosystem/
```

可能包含：

```text
schemas.py
mapper.py
weights.py
validators.py
fixtures.py
```

但当前不要急着实现。

### 17.2 Future API shape

未来如果需要 API，可考虑：

```text
GET /cases/{case_id}/opinion-ecosystem/preview
POST /cases/{case_id}/opinion-ecosystem/recompute
GET /cases/{case_id}/opinion-ecosystem/validation
```

边界：

```text
这些 API 只能使用已有 case Evidence。
不得 fetch URL。
不得 scrape。
不得调用真实平台 API。
不得调用真实 LLM。
必须保留 coverage note / causality note / confidence note。
```

### 17.3 Future mapping migration path

推荐顺序：

```text
Phase 3D:
  mapping contract docs.

Phase 3E:
  frontend fixture validator / UI polish.

Phase 4A:
  backend schema-only draft, still mock/local.

Phase 4B:
  backend mapper using existing local EvidenceItem data only.

Phase 4C:
  frontend sandbox consumes backend local mapped output.

Phase 4D:
  real demo case using CSV/Excel / Manual URL / optional YouTube only.

Phase 5:
  calibration / historical replay / sensitivity analysis.
```

---

## 18. Validator contract / 验证器契约

前端 / 后端 validator 都应检查：

```text
权重范围 0–1
rejected evidence 不进入 active weights
duplicate_group_id 不重复放大
low-trust evidence 降权或 warning
PeopleCluster 不暴露 raw author_id / author_name
InfluenceCore 不被当成小球
DeconstructionCore 与普通 PeopleCluster 分离
EchoBox 有边界指标
ResponseTempo 有 recommendation_text / risk_notes
ReputationMemory 有 unresolved grievance / reactivation fields
UI 保留 mock / coverage / causality / no real action 文案
```

---

## 19. UI copy requirements / UI 文案要求

必须显示：

```text
Mock visual prototype
基于静态模拟数据
不代表全网全量覆盖
不代表因果确定
不执行真实平台动作
小球代表人群簇，不代表真实个人
InfluenceCore 代表观念 / 内容 / 媒体 / 官方 / 梗化核心，不是人群小球
```

推荐术语：

```text
同化
中立化
退出
反噬
解构
处理节奏
叙事降压
回音壁
破圈风险
人群簇
观念核心
静态模拟
```

避免术语：

```text
水军
控评
带节奏
压制
猎杀
洗白
操控
精准影响用户
最易被说服的人
```

---

## 20. Acceptance checklist / 验收清单

Phase 3D docs 完成后，应满足：

```text
[ ] EvidenceItem 输入字段契约明确。
[ ] EvidenceRole 分类明确。
[ ] SourceIdentity 与 InfluenceCore 分离明确。
[ ] PeopleCluster 不暴露个人身份。
[ ] EchoBox 是回音壁容器，而不是 UI 背景。
[ ] rejected / duplicate / low-trust 门控明确。
[ ] DeconstructionCore 不是洗白模块。
[ ] ResponseTempo 输出边界明确。
[ ] ReputationMemory 表达长期残留。
[ ] 未来 backend handoff 不要求现在实现。
[ ] 保留 no API / no fetch / no scrape / no real LLM / no MediaCrawler 边界。
```

---

## 21. Current next recommended step / 当前下一步建议

完成本文件入库后，下一步不建议直接接真实 Evidence。

更稳的下一步：

```text
Phase 3E:
  frontend mapper contract UI polish
  or frontend-only validator mini-test if existing test setup supports it

Phase 4A:
  backend schema-only draft
  no API calls
  no real Evidence mapping yet
  no real LLM
  no platform API
```

如果要准备真实 demo：

```text
先选择真实但低敏事件类型。
优先游戏 / 动漫 / 社区争议。
用 CSV/Excel / Manual URL / optional YouTube。
不要用 live 抖音/B站/小红书/微博 API。
不要抓取。
不要宣称全网全量覆盖。
```

---

## 22. Summary / 总结

本 Mapping Contract 的核心是：

```text
EvidenceItem 不是直接变成小球。
EvidenceItem 先被分类为角色，再进入不同模型对象。

KOL / 视频 / 文章 / 媒体 / 官方公告 / 梗化内容
→ InfluenceCore / DeconstructionCore

评论者 / 回复者 / 参与讨论的人群
→ PeopleCluster

同平台 / 同集合体 / 同圈层 / 同话题讨论边界
→ EchoBox

同化 / 中立化 / 退出 / 反噬 / 再激活
→ CampDynamics

澄清 / FAQ / 第三方说明 / 解构 / 等待观察
→ ResponseTempo

事件结束后的黑称、残留不满、再激活风险
→ ReputationMemory
```

这份契约用于把前端 mock prototype 向未来正式 Evidence 映射过渡，同时继续保留 Sentigraph 的核心边界：合规证据、匿名人群簇、可解释权重、透明不确定性、非操控式处理节奏。
