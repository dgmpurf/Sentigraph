# Internal Recording Rehearsal 8-minute Script

## Purpose

This is a longer internal rehearsal route for explaining C-end event browsing, Opinion Ecosystem generated-run display, B-end report sample value, and safety boundaries.

It does not call real APIs, real LLMs, collector jobs, or external websites.

## Exact Route Sequence

Primary:

1. `/#/demo`
2. `/#/public-events`
3. `/#/public-events/donglu-sunjihai-youth-football`
4. `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
5. click generated-run panel
6. `/#/reports/donglu-sunjihai-youth-football-sample`

Optional:

- `/#/public-events/request`
- `/#/opinion-ecosystem`
- `/#/public-events/helldivers-psn`
- `/#/reports/helldivers-psn-sample`
- `/#/external-collector`
- `/#/analysis-requests` only if backend has no visible 500

## 0:00-0:45 Positioning

Click: `/#/demo`.

Say:

> Sentigraph 是公共事件证据分析和解释原型。当前演示是本地 demo，不是 live crawling，不是全网全量，不是全平台全量，不是完整讨论线，不是官方验证，不是预测，也不是生产部署。

## 0:45-1:30 Source And Boundary

Say:

> 当前样本是 selected sample only。generated run 是本地 fixture 输出；它不会读取真实 exchange dir，不访问 private collector，不抓取 URL，不调用真实 API 或真实 LLM。

Pause: show local demo / no live fetch / not full-web labels if visible.

## 1:30-2:20 Event Plaza

Click: `/#/public-events`.

Say:

> 事件广场是本地 demo 事件入口，不是实时热榜。request / support 相关入口如果展示，也只是 mock，不代表真实需求量或自然热度。

## 2:20-3:20 Dong/Sun Detail

Click: `/#/public-events/donglu-sunjihai-youth-football`.

Say:

> 这个页面展示董路 / 孙继海青训争议的事件摘要、样本覆盖和进入生态沙盒/报告样例的路径。这里不是官方真相，也不是全网全平台覆盖。

## 3:20-5:10 Opinion Ecosystem Generated Run

Click:

1. `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
2. generated-run button

Say:

> 这一段展示最小 real-run 闭环的前端结果：用户显式点击后，前端展示后端本地 fixture generated run。它有 run schema、run id、模型版本、系数来源、校准状态、经验验证状态、human review required、boundary labels 和模块输出。

Boundary:

> PeopleCluster 是匿名聚合群体 / 行为代理，不是真实个人。InfluenceCore 是内容、叙事、官方、媒体或 meme 核心，不是人。ResponseStrategyComparison 只用于人工复核，不生成公开回应，不自动执行，不发布、不发送、不提交。

Fallback if generated-run click fails:

> 如果本地后端未启动或 generated-run route 不可用，本段立即停止录制，不用静态 UI 替代生成运行结果。记录为 P0/P1 级 rehearsal blocker，回到 pre-flight 修复。

## 5:10-6:20 B-end Report Sample

Click: `/#/reports/donglu-sunjihai-youth-football-sample`.

Say:

> B-end 报告样例用于说明专业审阅价值：证据覆盖、争议结构、风险节奏、回应窗口和建议动作框架。它不是 B-end report runtime，也不是自动生成交付。

## 6:20-6:50 Optional Request/Support Mock

Click only if pre-flight passed: `/#/public-events/request`.

Say:

> request / support 是 mock flow，用来测试用户是否愿意请求另一个事件分析。它不是真实投票系统，不代表真实热度，不涉及支付。

## 6:50-7:20 Optional Helldivers/default Comparison

Click only if useful:

- `/#/opinion-ecosystem`
- `/#/public-events/helldivers-psn`

Say:

> Helldivers 是另一个 selected public sample，用来比较英文游戏社区事件。它同样不是全网全量、不是官方验证、不是因果证明。

## 7:20-7:45 Optional External Collector Boundary

Click only if useful: `/#/external-collector`.

Say:

> 外部采集桥接只用于解释本地 package 来源边界。当前 rehearsal 不运行 collector，不访问 private collector，不读取真实 package rows。

## 7:45-8:00 Closing

Say:

> 本次 rehearsal 只证明本地 selected sample generated-run 展示和脚本路径可讲清楚。它不代表公开发布、生产部署、真实平台接入、真实 LLM、自动回应或自动执行。
