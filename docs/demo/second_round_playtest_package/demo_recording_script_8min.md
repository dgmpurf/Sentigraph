# 8-Minute Recording Script

Status: recording script only. No live APIs, real LLMs, collector jobs, production reports, or platform actions are involved.

## 0:00-0:45 Product Positioning

Say:

> Sentigraph 是公共事件证据分析与解释原型。它面向两类体验：C-end 用户理解一个公开事件，B-end 专业用户评估风险、回应节奏和沟通建议。

Boundary:

> 当前演示是本地 demo。它不是全网爬虫，不是实时平台监控，不是官方验证，不是因果证明，也不生成真实请求、投票、赞助或下载交付。

## 0:45-1:30 Evidence / Source Boundary

Say:

> 演示中的 Dong/Sun 和 Helldivers 都是 controlled candidate / selected public sample。Evidence Scale 或 coverage 只表示已导入或已选择样本的覆盖，不代表 full-web 或 full-platform coverage。

If showing governance:

> Local Exchange Reader 是 disabled-by-default metadata-only scaffold，不是真实 collector integration。Provider output is evidence, not truth.

## 1:30-2:30 C-End Flow

Click:

- `/#/demo`
- `/#/public-events`

Say:

> Guided demo 帮新用户走完整路径。Event Plaza 展示本地 demo 事件，不是真实热榜。这里需要观察用户是否会误以为它是 live monitor。

Pause:

- Show local-only search or filter copy if visible.

## 2:30-3:30 Dong/Sun Case

Click:

- `/#/public-events/donglu-sunjihai-youth-football`

Say:

> Dong/Sun 页面用于展示一个中文公共事件的样本解释：事件摘要、争议结构、证据覆盖、沙盒入口和报告入口。我们要观察用户是否理解它是 controlled candidate public sample。

## 3:30-5:00 Sandbox V2

Click:

- `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
- Show V2 ecology view.
- Click through T0-T6 controls.

Say:

> Sandbox V2 是 frontend-only local historical replay。它把历史样本映射成阶段、群体和叙事核心。PeopleCluster 小球是匿名聚合群体 / 行为代理，不是真实个人。InfluenceCore 是内容、叙事、官方、媒体、KOL 或 meme 核心，不是人群小球。

Pause:

- Show safety copy.
- Show mapping / metrics card if visible.

Boundary:

> 这里不是未来预测，不是因果证明，也不执行真实平台动作。

## 5:00-6:30 B-End Report Sample

Click:

- `/#/reports/donglu-sunjihai-youth-football-sample`

Say:

> B-end 报告样例面向 PR、MCN、品牌、体育媒体、社区运营或公共沟通团队。重点看证据覆盖、风险机会、回应节奏、建议动作和边界说明。

Ask during review:

- Which section feels sellable?
- Which section feels confusing?
- Is the response tempo useful?
- Is the boundary wording clear enough for a client-facing report?

## 6:30-7:15 Governance Boundary If Useful

Optional click:

- `/#/analysis-requests`

Say:

> 技术评审可以看治理链路：本地文件握手、review-only case、dedup preview、promotion gates、report/export gates。当前 public access / external delivery 仍是 gate，不是外部交付 runtime。

Boundary:

> No public URL, no signed URL, no file-byte route, no ZIP, no external delivery.

## 7:15-7:45 Planned-Only / Not Implemented

Say:

> 当前没有真实 Douyin / Bilibili / RSS / GDELT / vendor / LLM provider。Search Discovery 和相关 provider 仍是 mock/static 或 planning。OpenClaw 只能作为外部人工辅助，不是生产 ingestion。

## 7:45-8:00 Business Angle And Close

For C-end:

> 我们想验证普通用户是否愿意打开、理解和分享一个事件页，也是否会请求另一个事件分析。

For B-end:

> 我们想验证这套证据解释、回应节奏和报告结构，是否能帮助公关、运营、内容和品牌团队更透明地判断风险与行动窗口。
