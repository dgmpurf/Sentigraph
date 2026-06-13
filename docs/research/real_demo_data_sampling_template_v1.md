# Sentigraph Phase 4B：真实 Demo 数据采样模板 v1

**文件用途**：为第一版真实 demo 准备一套可手工填写的 CSV/Excel 数据采样模板。  
**推荐 demo 事件**：Helldivers 2 / PSN 账号绑定争议。  
**性质**：采样与导入模板，不是 crawler，不是 live API，不是全网全量覆盖。  
**推荐放置位置**：`docs/research/real_demo_data_sampling_template_v1.md`

---

## 1. 这一步要解决什么

Phase 4A 已经选出真实 demo 候选事件。Phase 4B 的目标是准备一个可以实际填写的采样模板，让公开材料、评论样本、官方说明、媒体报道、社区梗化内容能够进入 Sentigraph 的 Evidence Layer，并在后续映射到：

```text
EvidenceItem
→ Influence Core / Narrative Core
→ EchoBox
→ People Cluster
→ Camp Dynamics
→ Deconstruction Core
→ Response Tempo
→ Reputation Memory
```

本阶段仍然不做：

```text
自动抓取
URL fetch
平台 API
RSS/GDELT/Search live provider
LLM 分析
MediaCrawler
OpenClaw production ingestion
真实 backend mapper
```

---

## 2. 推荐文件

建议同时保留两个模板文件：

```text
docs/research/real_demo_data_sampling_template_v1.md
docs/templates/real_demo_evidence_sampling_template_v1.xlsx
```

其中：

```text
real_demo_data_sampling_template_v1.md
= 采样说明、字段解释、边界和工作流

real_demo_evidence_sampling_template_v1.xlsx
= 实际填写的 Excel/CSV 模板
```

如果不想把 `.xlsx` 放进 repo，也可以只保留本说明文档，把 Excel 作为本地工作文件使用。

---

## 3. 采样原则

### 3.1 只采公开材料

允许：

```text
公开官方公告
公开媒体报道
公开社区帖子
公开视频 / 文章 / 评论区摘要
公开评论样本
公开梗化 / 二创 / 社区符号样本
公开互动指标快照
```

禁止：

```text
私信
登录后不可见内容
cookie / token / session
账号池数据
验证码绕过数据
自动抓取来的数据
非公开个人资料
```

### 3.2 不做全量声明

所有 demo 页面和报告必须保留：

```text
本分析基于手工采样的公开证据。
不代表全网全量覆盖。
不代表全平台完整评论。
不代表因果确定。
不执行真实平台动作。
```

### 3.3 人群只做匿名簇

评论者不能在公开 demo 中展示原始用户名、uid 或可识别身份。

推荐做法：

```text
raw author_id / author_name → 仅用于本地匿名聚合
public demo → PeopleCluster / 人群簇标签
```

例如：

```text
核心玩家反对群体
证据敏感中立群体
温和支持群体
高情绪反对群体
疲劳围观群体
```

---

## 4. 采样配比建议

第一版真实 demo 不需要全量数据。建议先采：

| 类型 | 建议数量 | 用途 |
|---|---:|---|
| 官方 / 平台公告 | 2–5 | 官方 Influence Core、事件时间线 |
| 媒体 / 新闻报道 | 3–8 | 中立解释、时间线、外部扩圈 |
| 创作者视频 / 文章 / 帖子 | 5–12 | 反方/正方/中立 Influence Core |
| 社区主帖 / 论坛串 | 5–10 | EchoBox 和社区回音壁 |
| 评论 / 回复样本 | 100–300 | PeopleCluster 和阵营分布 |
| 梗化 / 二创 / 解构内容 | 3–10 | DeconstructionCore / ReputationMemory |
| 指标快照 | 5–20 | 热度、破圈、生命周期判断 |

第一版最小可运行样本：

```text
5 个 Influence Core
3 个 EchoBox
100 条评论/回复样本
3 个 Deconstruction / ReputationMemory 信号
```

---

## 5. Evidence_Items 主表字段说明

模板主表是 `Evidence_Items`。关键字段如下。

### 5.1 基础字段

```text
sample_id
case_id
event_stage
platform
evidence_type
evidence_role
source_type
source_url
source_title
published_at
collected_at
```

建议 `case_id`：

```text
helldivers2_psn_demo
```

### 5.2 内容与关系字段

```text
root_id
parent_id
content_excerpt_or_summary
claim_summary
```

解释：

```text
root_id:
一个视频、帖子、文章、官方公告、评论区的根节点。

parent_id:
评论/回复所属的上级节点。

content_excerpt_or_summary:
短摘录或人工摘要。公开 demo 不建议保留过长原文。
```

### 5.3 立场与语义字段

```text
stance_label
stance_strength
sentiment_intensity
evidence_strength
logic_strength
emotional_intensity
extremity_score
```

建议使用 0–1 之间的分数。

```text
stance_label:
support / neutral / oppose / mixed / unknown

stance_strength:
立场强度

sentiment_intensity:
情绪强度

evidence_strength:
证据强度

logic_strength:
推理清晰度 / 逻辑强度

extremity_score:
极端程度
```

这些分数第一版可以人工估计，必须标记 `parameter_source=manual_parameter` 或 `inferred_proxy`。

### 5.4 互动指标字段

```text
view_count
like_count
comment_count
reply_count
share_count
repost_count
```

如果没有指标，留空。不要编造。

### 5.5 证据治理字段

```text
acquisition_mode
provenance_type
verification_status
trust_label
review_status
duplicate_group_id
duplicate_count
risk_flags
```

规则：

```text
rejected → 不进入 active weights
marked_weak / low trust → 降权
duplicate_group_id 相同 → 不重复放大声量
needs_review → 显示复核提示
```

### 5.6 隐私与输出字段

```text
raw_identity_present
anonymization_required
include_in_demo
notes
```

如果内容中含原始用户名 / uid / 可识别个人信息：

```text
raw_identity_present = Yes
anonymization_required = Yes
```

公开 demo 时必须匿名化。

---

## 6. Influence Core 判定规则

一个 EvidenceItem 可以成为 Influence Core，如果满足任意条件：

```text
它是官方公告、媒体报道、创作者视频、创作者文章、社区主帖、梗化内容；
它是 root 内容，且有大量评论/回复；
它被多个社区、评论或内容反复引用；
它是事件导火索或二次升级点；
它是第三方解释或官方回应；
它具有明显解构/梗化潜力。
```

不要把普通评论随意判成 Influence Core。普通评论默认只是 PeopleCluster 信号，除非它爆火、被引用、成为导火索。

---

## 7. EchoBox 判定规则

EchoBox 是回音壁容器，不是 UI 边框。

第一版可以按：

```text
platform + root_id / InfluenceCore + topic
```

生成 EchoBox。

例如：

```text
Steam 玩家核心回音壁
Reddit-like 社区争议区
YouTube-like 创作者评论区
媒体解释外圈
社区梗化区
```

EchoBox 需要记录：

```text
echo_chamber_score
carrying_capacity
saturation_ratio
permeability_score
internal_reinforcement
breakout_risk
fatigue_rate
```

---

## 8. PeopleCluster 判定规则

评论/回复样本进入 PeopleCluster，不展示个人身份。

推荐第一版聚类方式：

```text
stance_label
+ comment topic / claim_summary
+ evidence_sensitivity
+ emotion_load
+ fatigue
```

常见簇：

```text
核心玩家反对群体
证据敏感中立群体
温和支持群体
高情绪反对群体
疲劳围观群体
解构接受群体
潜伏不满群体
```

---

## 9. DeconstructionCore / ReputationMemory 采样

需要采样：

```text
梗图 / 二创 / 社区口号 / 自嘲内容 / 社区共创符号
```

并记录：

```text
是否降低敌意
是否给温和反对者台阶
是否保留长期黑称 / 污名
是否可能未来再激活
```

注意：

```text
解构不是洗白。
解构不等于问题解决。
梗化可能短期降压，也可能长期固化负面标签。
```

---

## 10. 推荐工作流

```text
1. 建立 case_id
2. 采 2–5 条官方/平台/时间线证据
3. 采 3–8 条媒体/解释类证据
4. 采 5–12 条创作者视频/帖子/文章
5. 每个核心内容下手工采样 10–30 条评论/回复
6. 记录互动指标快照
7. 标记 stance / trust / review / duplicate
8. 删除或匿名化原始身份
9. 标记哪些进入 demo
10. 导入 Sentigraph CSV/Excel，进入 Evidence Layer
```

---

## 11. 质量检查

采样完成后检查：

```text
是否包含正/中/反三类评论
是否有官方/反方/中立/解构核心
是否有低可信和 rejected 示例
是否有 duplicate_group_id 示例
是否有 coverage note
是否无真实个人身份暴露
是否无私信、cookie、登录后数据
是否没有把样本说成全量
```

---

## 12. 后续 Phase

```text
Phase 4B：
完成采样模板。

Phase 4C：
手工填入第一批真实公开样本。

Phase 4D：
通过现有 CSV/Excel import 导入 Sentigraph Evidence Layer。

Phase 4E：
用导入 Evidence 生成 demo 报告和舆论生态沙盒映射。
```

注意：Phase 4D / 4E 仍然不代表全网全量，也不代表真实平台 live API 已接入。
