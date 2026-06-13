# GitHub 舆情系统与多智能体推演项目参考扫描

**建议存放位置**：`docs/research/github_public_opinion_systems_scan.md`  
**检索日期**：2026-06-13  
**用途**：为 Sentigraph / 归墟舆情分析后续的 C 端公共事件推演、B 端专业舆情服务、复杂权重体系与小球 Agent 沙盒设计提供参考。  
**性质**：这是研究参考文档，不代表 Sentigraph 将复制这些项目，也不代表其中的采集、爬虫、LLM、平台接入或预测能力已经在 Sentigraph 中实现。

---

## 1. 用途

本文扫描若干 GitHub 上与“舆情分析、公共事件监测、多智能体推演、趋势雷达、情感分析、社会事件检测”相关的开源项目，目的是帮助 Sentigraph 在产品设计和架构路线中区分：

```text
哪些产品叙事值得参考；
哪些 UI / 报告 / 推演表达值得参考；
哪些算法或数据结构值得作为后续研究入口；
哪些采集、爬虫、平台覆盖、真实 API、LLM 黑箱推演路线不能照搬。
```

本文不是竞品测评，不评价这些项目的真实可用性、合规性或工程质量；只从 Sentigraph 当前边界出发，提取对本项目有价值的设计启发。

---

## 2. Sentigraph 当前边界

本报告必须服从 Sentigraph 当前 Project Source 边界：

```text
Sentigraph 不是 full-web crawler / 全网自动爬虫。
当前真实官方 API 路径只有 optional local YouTube。
Douyin / Bilibili / Xiaohongshu / Reddit / Weibo 真实接入仍 pending。
Search Discovery / RSS / GDELT 当前是 mock/static，不是 live provider。
Vendor POC 是离线样本映射与评分，不是真实 vendor adapter。
Vendor data 默认 vendor_attested / medium_low，不是官方验证。
LLM provider 仍为 mock。
MediaCrawler 未集成。
OpenClaw / 龙虾只能作为外部人工辅助，不是 production ingestion。
Evidence Scale / Coverage 只表示已导入/可用证据覆盖，不代表全网/全平台覆盖。
```

Source 08 已经把下一阶段方向定义为：

```text
EvidenceItem
→ Content Aggregate
→ Anonymous Actor
→ Community / KOL / Bridge Node
→ Agent Weight
→ Agent-Based Sandbox
→ Scenario Comparison / Report
```

因此，本报告里的项目只能作为参考，不应改变 Sentigraph 的合规数据路线。

---

## 3. 核心参考项目

### A. BettaFish / 微舆

**Repository**：https://github.com/666ghj/BettaFish

#### 公开定位

BettaFish 自称“微舆：人人可用的多 Agent 舆情分析助手”，公开 README 中强调多智能体舆情分析、还原舆情原貌、预测未来走向和辅助决策。其产品叙事非常接近“普通用户也能发起舆情分析”的 C 端表达。

#### 可参考点

```text
1. C 端产品叙事
   “人人可用”“像聊天一样提出分析需求”“自动生成报告”这类表达，对 Sentigraph 的公共事件入口有参考价值。

2. 多 Agent 报告流程
   Query / Media / Insight / Report 等分工可以作为 Sentigraph 未来多模块报告编排的参考。

3. 公开报告样例
   可研究其报告结构、章节组织、摘要方式、图表表达和“事件解释”风格。

4. C 端拉新方式
   公开示例、演示视频、案例报告、赞助/支持等方式，对 Sentigraph 的公开事件页和 demo 传播有参考意义。
```

#### 不可照搬点

```text
1. 不照搬 full-web crawler / 全域监控叙事。
2. 不照搬“覆盖 30+ 社媒 / 数百万评论 / 7x24 小时 AI 爬虫集群”等能力表述。
3. 不照搬任何不清晰的 crawler / scraper / 搜索抓取 / 网页内容抓取路线。
4. 不把 Sentigraph 宣传成“全平台全量评论采集”。
5. 不让 Codex 基于 BettaFish 路线实现 crawler、MindSpider、账号池、cookies、验证码绕过、代理抓取等能力。
```

#### 与 Sentigraph 的差异

BettaFish 更像：

```text
多 Agent 舆情报告 + 全域采集叙事 + C 端可用入口
```

Sentigraph 应该更像：

```text
合规 Evidence Layer
+ Trust / Dedup / Review / Audit
+ Content Aggregate 权重
+ Anonymous Actor 权重
+ Community / KOL / Bridge 分析
+ Agent-Based 小球沙盒
+ C 端公开事件页
+ B 端专业报告
```

Sentigraph 的差异化不应是“我抓得更多”，而应是：

```text
我能解释证据来源、可信度、重复折叠、参与者权重、集合体热区、阵营结构与传播动力学。
```

---

### B. MiroFish

**Repository**：https://github.com/666ghj/MiroFish

#### 公开定位

MiroFish 自称基于多智能体技术的新一代 AI 预测引擎。其 README 强调从现实种子信息构建“平行数字世界”，让具备人格、记忆与行为逻辑的智能体交互演化，并通过“上帝视角”动态注入变量来推演未来走向。

#### 可参考点

```text
1. 数字沙盘叙事
   “平行数字世界”“上帝视角”“百战模拟”等表达，和 Sentigraph 的小球沙盒视觉方向有相通之处。

2. 预测报告 + 可交互世界
   Sentigraph 未来可以同时输出：
   - 可视化小球沙盒
   - 事件走势报告
   - 参数/假设说明

3. 多主体动态演化
   对 Sentigraph 的 Agent-Based Simulation 有概念启发。

4. C 端可传播性
   将复杂推演包装成可观看、可交互的体验，这是 Sentigraph C 端公开事件页需要学习的。
```

#### 不可照搬点

```text
1. 不把 Sentigraph 做成纯 LLM agent 黑箱模拟。
2. 不声称“精准预测未来”。
3. 不让每个 agent 变成高自由度生成式人格，第一版应保持可解释、可验证、可审计。
4. 不接真实 LLM social simulation，当前 Sentigraph LLM 仍为 mock。
5. 不忽略 Evidence Layer、证据可信度、参数来源与不确定性。
```

#### 与 Sentigraph 的差异

MiroFish 更像：

```text
通用多智能体预测引擎 / 数字世界沙盘
```

Sentigraph 应该更像：

```text
证据驱动的公共事件舆论结构分析与传播推演系统
```

Sentigraph 的小球沙盒不应依赖“智能体自由发挥”，而应基于：

```text
EvidenceItem
ContentAggregate
AnonymousActor
Community/KOL/Bridge
公开行为代理权重
模型假设参数
不确定性标注
```

---

### C. POA Multi-Agent System

**Repository**：https://github.com/isswu/poa-multi-agent

#### 公开定位

POA Multi-Agent System 是一个基于 OpenAI Agents 框架的 public opinion analysis multi-agent system。README 中提到面向抖音、小红书、Bilibili 等中文社交平台，使用多 Agent 做数据收集、情感分析、趋势检测、风险识别和报告生成。

#### 可参考点

```text
1. 多 Agent 角色拆分
   Coordinator Agent、Data Collection Agent、Content Analysis Agent、Report Generation Agent、Decision Support Agent 等命名可作为模块划分参考。

2. FastAPI + React 工程结构
   与 Sentigraph 当前前后端结构有一定相似性，可参考工程分层和 API/前端组织。

3. Chat interface
   面向普通用户或客户的自然语言分析入口可以作为中后期 C/B 双端交互参考。

4. 报告生成流程
   可参考如何从分析结果到 executive summary / detailed analytics。
```

#### 不可照搬点

```text
1. 不假设抖音、小红书、B站数据采集已经合规可用。
2. 不接 OpenAI Agents 或真实 LLM。
3. 不把 Data Collection Agent 变成真实平台抓取器。
4. 不实现 real-time live analysis，除非真实数据源、权限、配额和合规 gates 完成。
```

#### 与 Sentigraph 的差异

POA 更偏：

```text
OpenAI Agents orchestrated public opinion analysis
```

Sentigraph 当前应该保持：

```text
mock/default + optional YouTube real
Evidence-first
LLM mock
平台真实接入 pending
```

未来可借鉴其 Agent 角色命名，但底层必须保持 Sentigraph 的 Evidence governance 与 Source boundary。

---

### D. TrendRadar

**Repository**：https://github.com/SANSAN0/TRENDRADAR

#### 公开定位

TrendRadar 是 AI-driven public opinion & trend monitor，主打多平台聚合、RSS、热点筛选、AI 分析简报和多渠道推送。README 还强调支持 MCP 架构、数据本地/云端自持、微信/飞书/钉钉/Telegram/邮件等渠道推送。

#### 可参考点

```text
1. 事件广场 / 热点雷达
   Sentigraph C 端可以参考“热点卡片、趋势摘要、关键词筛选、事件生命周期”的表达。

2. 推送与订阅
   未来 B 端可以参考风险提醒、日报、周报、事件更新通知。

3. MCP / AI 对话入口
   未来可以把 Sentigraph 分析结果作为工具提供给内部 Copilot 或客户侧分析助手，但这应晚于核心模型和合规边界。

4. 本地积累数据再分析
   TrendRadar 说明 AI 分析依赖本地已积累新闻数据，而不是直接实时查询网络。这个表述对 Sentigraph 很有启发：公开页面必须说明数据范围和时效限制。
```

#### 不可照搬点

```text
1. 不声称 Sentigraph 已经接入真实 RSS/GDELT/search provider。
2. 不把 mock/static Search Discovery 说成实时热榜搜索。
3. 不复制任何 crawler / live fetch 行为。
4. 不用 TrendRadar 的“聚合多平台热点”叙事掩盖 Sentigraph 当前数据限制。
```

#### 与 Sentigraph 的差异

TrendRadar 更像：

```text
新闻/热点/RSS 聚合 + AI 摘要 + 推送工具
```

Sentigraph 更应该强调：

```text
事件证据治理
参与者/集合体权重
正中反结构
小球传播推演
B 端公关决策报告
```

TrendRadar 对 Sentigraph 的最大启发不是“数据采集”，而是：

```text
C 端事件入口、趋势卡片、提醒机制、热点生命周期表达。
```

---

### E. PublicOpinion

**Repository**：https://github.com/CodeAsPoetry/PublicOpinion

#### 公开定位

PublicOpinion 是较传统的舆情分析系统，公开描述包括爬虫、数据清洗、文本摘要、主题分类、情感倾向识别和可视化。

#### 可参考点

```text
1. 传统舆情 pipeline
   crawler / cleaning / summarization / topic classification / sentiment / visualization 是早期舆情系统常见链路。

2. 数据清洗与人工 review
   其 README 中涉及微博评论、搜狐评论等数据清洗和标签构造，能提醒 Sentigraph 重视导入数据清洗、编码、去重、人工复核。

3. 传统可视化
   可以作为对照：Sentigraph 不应只停留在柱状图、词云、情感饼图。
```

#### 不可照搬点

```text
1. 不回退成“爬虫 + NLP dashboard”。
2. 不复制爬虫采集路线。
3. 不把传统情感分类当成 Sentigraph 的核心壁垒。
```

#### 与 Sentigraph 的差异

PublicOpinion 代表传统舆情系统：

```text
采集 → 清洗 → NLP 分类 → 可视化
```

Sentigraph 的目标应升级为：

```text
合规证据 → 证据治理 → 人群/集合体权重 → 传播动力学 → 沙盒推演 → 决策报告
```

---

### F. Weibo_PublicOpinion_AnalysisSystem

**Repository**：https://github.com/Astianjy/Weibo_PublicOpinion_AnalysisSystem

#### 公开定位

该仓库页面显示其与微博舆情分析系统相关，同时 GitHub 页面标注其 forked from BettaFish。公开信息有限，适合作为“微博舆情系统命名和传统平台专属舆情方向”的弱参考。

#### 可参考点

```text
1. 微博单平台舆情系统的产品命名和功能方向。
2. 单平台监控、趋势、情感和可视化的传统结构。
3. 可作为“不要过度依赖某一平台”的反例参考。
```

#### 不可照搬点

```text
1. 不假设微博数据可以直接抓取。
2. 不复制账号/crawler/登录态采集假设。
3. 不声称 Sentigraph 已接入 Weibo。
```

#### 与 Sentigraph 的差异

Sentigraph 不应成为单平台微博工具。微博、抖音、B站、小红书等真实接入都必须等待官方权限、供应商合同或合规 POC 后再推进。

---

### G. SocialED

**Repository**：https://github.com/RingBDStack/SocialED

#### 公开定位

SocialED 是一个 Python library for social event detection。README 中说明它包含 19 个检测算法、15 个数据集、统一 API、预处理、图构建、训练与预测接口，并且下游应用包括 crisis management、public opinion monitoring、fake news detection 等。

#### 可参考点

```text
1. 社会事件检测算法库
   可作为未来事件发现、事件聚类、话题演化、异常检测的研究入口。

2. 图与文本结合
   Sentigraph 未来的 Content Aggregate / Community / Bridge 分析可能需要类似图结构和文本聚类方法。

3. 事件检测 benchmark
   可参考其算法列表和数据集组织方式，未来做 Sentigraph 自己的 historical replay / validation。
```

#### 不可照搬点

```text
1. 不把 SocialED 当产品模板。
2. 不把算法库接入等同于真实舆情系统完成。
3. 不在当前阶段引入复杂 GNN / event detection pipeline，除非已有足够数据和验证设计。
```

#### 与 Sentigraph 的差异

SocialED 是算法/研究库；Sentigraph 是产品系统。

SocialED 对 Sentigraph 的价值主要在：

```text
未来事件发现 / 事件聚类 / 社会事件检测算法参考。
```

而 Sentigraph 当前更需要先完成：

```text
Content Aggregate schema
Anonymous Actor schema
Agent Weight schema
小球沙盒视觉原型
Evidence → Weight 映射
```

---

### H. UIE-SentimentAnalysisWeb

**Repository**：https://github.com/JIANG-HS/UIE-SentimentAnalysisWeb

#### 公开定位

UIE-SentimentAnalysisWeb 是基于 UIE 的舆论情感分析 Web 系统，技术栈包括 FastAPI、UIE、Vue、ElementUI、ECharts，支持单文本属性级情感分析、上传 txt 批量情感分析和可视化展示。

#### 可参考点

```text
1. 轻量前后端情感分析 Web
   FastAPI + Vue + ECharts 的组合可以作为轻量展示参考。

2. 属性级情感分析展示
   Sentigraph 未来在“核心争议点 / 属性 / 观点 / 情感”展示上可参考其可视化思路。

3. 批量文本分析体验
   对 CSV/Excel/文本导入后的 preview 和 batch analysis 有启发。
```

#### 不可照搬点

```text
1. 不把 Sentigraph 简化成批量情感分析工具。
2. 不把词云/柱状图/情感分类当作最终产品壁垒。
3. 不接真实 UIE 模型或外部 LLM，除非明确进入模型接入阶段。
```

#### 与 Sentigraph 的差异

UIE-SentimentAnalysisWeb 是文本情感分析工具；Sentigraph 应该覆盖：

```text
证据治理
内容集合体
匿名参与者
群体结构
传播推演
专业报告
```

---

## 4. Comparative table

| Project | Main orientation | Useful for Sentigraph | Must not copy | Sentigraph differentiation |
|---|---|---|---|---|
| BettaFish / 微舆 | 多 Agent 舆情分析与报告，C 端可用叙事 | 公开事件分析入口、多 Agent 报告流程、案例报告表达 | 全域爬虫、全平台覆盖、数百万评论、7x24 抓取叙事 | Evidence governance + Actor/Aggregate 权重 + 小球沙盒 |
| MiroFish | 多智能体预测引擎、数字沙盘 | 小球沙盒叙事、平行世界/上帝视角、交互式推演 | 纯 LLM agent 黑箱、预测确定性、人格化大规模自由生成 | 证据驱动、参数可解释、假设可审计、输出有不确定性 |
| POA Multi-Agent | OpenAI Agents 舆情分析平台 | Agent 角色拆分、FastAPI/React 架构、Chat interface | 真实平台采集假设、OpenAI real calls、Data Collection Agent 抓取化 | LLM mock、平台 pending、Evidence-first |
| TrendRadar | 热点/RSS/新闻聚合、AI 摘要、推送 | 事件广场、趋势卡片、热点生命周期、通知机制 | 把 mock Search/RSS/GDELT 说成 live provider | 舆论结构 + 权重 + 沙盒推演，而非纯热点聚合 |
| PublicOpinion | 传统舆情 pipeline | 数据清洗、情感/主题分类、传统可视化 | 爬虫 + NLP dashboard 路线 | 从情绪统计升级到传播动力学与决策报告 |
| Weibo_PublicOpinion_AnalysisSystem | 微博/单平台舆情方向参考 | 单平台监控结构、微博方向弱参考 | 微博抓取/登录态/账号假设 | 不声称 Weibo real integration，保持 pending |
| SocialED | 社会事件检测算法库 | 事件发现、事件聚类、图/文本算法、future validation | 把算法库当产品模板，当前阶段引入重 GNN | 产品系统 + Evidence Layer + ABM 沙盒 |
| UIE-SentimentAnalysisWeb | 属性级情感分析 Web | 轻量 FastAPI/Vue/ECharts、批量文本可视化 | 只做批量情感分析、词云/柱状图即终点 | 情感只是输入层，核心是人群/集合体/传播推演 |

---

## 5. Product takeaways for Sentigraph

### 5.1 C 端可以参考 BettaFish + TrendRadar

Sentigraph 的 C 端不是专业后台，而是普通用户能看懂、愿意分享的公共事件入口。

可以参考：

```text
事件广场
事件卡片
热点/争议度/风险等级
公开事件摘要
公众投票 / 请求分析
赞助分析 / 优先推演队列
小球沙盒动画
公开报告摘要
```

但必须保留：

```text
数据来源说明
覆盖边界
是否赞助/用户请求标注
不代表全网全量
不代表事实裁判
不代表预测确定
```

### 5.2 推演表达可以参考 MiroFish，但 Sentigraph 不能变成纯 LLM agent 沙盘

MiroFish 对 Sentigraph 的启发是：

```text
把复杂模型变成可观看、可交互、可解释的数字沙盘。
```

但 Sentigraph 第一版小球沙盒应是：

```text
mock/static 或 Evidence-derived 数据
可解释参数
固定规则
可重放
可审计
不接真实 LLM
不声称因果确定
```

### 5.3 传统 NLP 系统只做基础参考

PublicOpinion 和 UIE-SentimentAnalysisWeb 提醒我们：情感分析、主题分类、文本摘要、词云、柱状图是必要基础，但不是 Sentigraph 的终局。

Sentigraph 的核心应该从：

```text
这批评论是正面还是负面？
```

升级到：

```text
哪些人群在说？
哪些集合体在带动？
哪些社区形成回音壁？
哪些桥接节点让事件跨圈层？
正中反权重如何变化？
不同透明回应方案下，热区和风险是否可能变化？
```

### 5.4 SocialED 可作为未来算法参考，但不是当前 MVP

SocialED 对长期有价值，尤其是：

```text
事件发现
事件聚类
社交消息图构建
不确定性事件检测
算法 benchmark
```

但当前更优先的是：

```text
小球沙盒视觉原型
ActorWeight schema
ContentAggregateWeight schema
Community/KOL/Bridge schema
Evidence → Weight 映射
C 端公开事件页
B 端报告样例
```

---

## 6. Sentigraph 建议差异化路线

综合这些参考项目，Sentigraph 不应走以下路线：

```text
全网 crawler 项目
全平台评论抓取工具
简单情感分析 dashboard
纯 LLM 多智能体黑箱预测
RSS/新闻聚合推送工具
单平台微博/抖音/小红书监控工具
```

Sentigraph 更适合的路线是：

```text
Evidence Layer
+ Content Aggregate Weight
+ Anonymous Actor Weight
+ Community / KOL / Bridge analysis
+ Agent-Based Sandbox
+ C-end public event page
+ B-end professional report
```

一句话：

> Sentigraph 的核心竞争力不应是“抓到最多数据”，而应是“把合规证据转成可解释的舆论结构、权重、热区、传播走势和决策参考”。

---

## 7. 与 Source 08 的关系

Source 08 已经定义：

```text
Agent-Based Simulation / 小球沙盒
Actor Weight Model
Content Aggregate Weight Model
Community / KOL / Bridge Node
Opinion Dynamics 模型
伦理边界
C 端 + B 端双轨定位
```

本文只是 GitHub 参考项目扫描，不表示 Sentigraph 已经实现：

```text
Actor Weight Model
Content Aggregate Weight Model
Community / KOL Weight Model
Agent-Based 小球沙盒
Evidence → Actor 自动聚合
真实历史事件 replay validation
```

后续模型和 Codex 必须继续区分：

```text
research reference
project source
implemented code
mock/static prototype
real provider / production feature
```

---

## 8. 对复杂权重体系的启发

用户明确希望 Sentigraph 权重体系可以做复杂，而不仅是简单评论数或情感分类。因此后续权重可以按四层组织。

### 8.1 Evidence Weight

已在当前系统中存在：

```text
trust_score
trust_label
verification_status
provenance_type
review_status
duplicate_group_id
duplicate_count
risk_flags
```

作用：

```text
判断证据可信度、是否重复、是否进入分析、是否需要复核。
```

### 8.2 Content Aggregate Weight

后续新增：

```text
exposure_potential
engagement_intensity
participation_depth
controversy_score
sentiment_intensity
echo_chamber_score
bridge_score
amplification_score
risk_score
heat_score
```

作用：

```text
判断哪个视频/帖子/文章/评论区/话题标签是热区或风险区。
```

### 8.3 Anonymous Actor Weight

后续新增：

```text
stance_score
stance_strength
activity_weight
expression_intensity
influence_weight
reply_centrality
amplification_tendency
bridge_score
repetition_score
volatility_proxy
conformity_proxy
contrarian_proxy
abnormality_risk
```

注意：这些是公开行为代理指标，不是人格诊断或真实心理测量。

### 8.4 Simulation Agent Weight

小球沙盒需要：

```text
attention_budget
fatigue
confidence_radius
action_threshold
stubbornness
source_trust_profile
community_id
stance_label
influence_weight
activity_weight
emotion_intensity
```

作用：

```text
在小球沙盒中模拟关注、情绪、表达倾向、立场状态、回音壁、桥接传播和热区变化。
```

---

## 9. 真实 Demo 策略

用户希望 demo 使用真实事件。建议采用：

```text
真实事件 + 合规导入证据
```

而不是：

```text
真实平台 live API / 真实全网搜索 / 未授权抓取
```

可接受路径：

```text
1. YouTube official API optional real path，如果事件适合 YouTube。
2. 手工整理的真实公开评论 CSV/Excel。
3. Manual URL evidence。
4. 供应商脱敏样例。
5. 公开新闻、报告、评论样本，但必须标注来源和覆盖边界。
```

真实 demo 页面必须说明：

```text
本分析基于已导入/可用证据，不代表全网全量覆盖。
不同平台数据可得性不同。
低可信或人工导入证据已做标记。
模拟结果是 scenario-conditioned，不代表因果确定或未来保证。
```

---

## 10. 推荐后续步骤

### Step 1：保存本文为 research note

```text
docs/research/github_public_opinion_systems_scan.md
```

### Step 2：不要基于这些项目实现 crawler

尤其不要从 BettaFish、PublicOpinion、微博类系统中引入：

```text
cookies
账号池
验证码绕过
反爬绕过
代理抓取
隐藏接口
高频 crawler
MediaCrawler 主线集成
OpenClaw production ingestion
```

### Step 3：下一步代码方向只允许二选一

更安全的第一步是：

```text
A. frontend-only mock 小球沙盒视觉原型
```

或：

```text
B. backend schema-only mock ActorWeight / ContentAggregateWeight / CommunityWeight
```

两者都必须：

```text
不调用外部 API
不 fetch URL
不 scrape
不接真实 LLM
不接真实平台
不接真实 search/RSS/GDELT
不接 vendor API
```

### Step 4：同步准备真实 demo 数据

真实 demo 应从合规证据开始：

```text
真实事件链接清单
公开评论样本 CSV/Excel
Manual URL evidence
Evidence trust/review 标记
coverage note
uncertainty note
```

---

## 11. Codex 落地建议

如果需要 Codex 把本文放进 repo，应使用 docs-only prompt：

```text
Docs-only. Create docs/research/github_public_opinion_systems_scan.md with the provided content. Do not modify backend/frontend code. Do not call APIs. Do not fetch URLs. Do not scrape. Do not integrate MediaCrawler/OpenClaw. Do not call real LLM. Do not read or print secrets. Run git status only. No tag needed.
```

Codex 输出必须确认：

```text
No code changed.
No real APIs called.
No URL fetching/scraping.
No MediaCrawler integration.
No OpenClaw production integration.
No real LLM.
No secrets read or printed.
Recommended tag: no tag needed.
```
