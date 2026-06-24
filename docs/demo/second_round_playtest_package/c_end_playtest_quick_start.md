# C-End Playtest Quick Start

Status: C-end demo guidance only. This document does not implement runtime behavior or collect live data.

## Goal

Check whether normal users understand what Sentigraph is, what the public event experience shows, and where the demo boundaries are.

## Route Flow

1. `/#/demo`
2. `/#/public-events`
3. `/#/public-events/donglu-sunjihai-youth-football`
4. `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`
5. `/#/public-events/request`
6. Optional: `/#/reports/donglu-sunjihai-youth-football-sample`

## Step Prompts

### 1. Guided Demo Page

Ask:

- 你觉得这个页面在引导你做什么？
- 你会先点哪里？
- 你是否能看出这是本地 demo，而不是线上真实平台？

Clarify:

- 这里的搜索或筛选只用于本地 demo 事件，不进行全网搜索、抓取或实时平台监控。

### 2. Event Plaza

Ask:

- 你觉得这些事件卡片代表什么？
- 你会打开哪个事件？为什么？
- 你是否误以为这里是实时热榜？

Clarify:

- Event Plaza 是公共事件入口原型，不是真实热榜，不代表自然公共舆论热度。

### 3. Dong/Sun Event Detail

Ask:

- 你能说出这个事件页在展示什么吗？
- 你是否能看出这是 controlled candidate public sample？
- 你是否误以为它覆盖了全网、全平台或完整讨论线程？

Clarify:

- Dong/Sun 是受控候选公共样本，不是全网抓取结果，也不是官方验证结论。

### 4. Opinion Ecosystem Sandbox V2

Ask:

- PeopleCluster 是什么？
- InfluenceCore 是什么？
- 你是否能区分“小球”和核心节点？
- 你是否误以为这是未来预测？

Clarify:

- PeopleCluster 是匿名聚合群体 / 行为代理，不是真实个人。
- InfluenceCore 是内容、叙事、官方、媒体、KOL 或 meme 核心，不是人群小球。
- Sandbox V2 是 frontend-only local historical replay，不是因果证明，也不执行真实平台动作。

### 5. Request / Vote Mock

Ask:

- 你觉得请求分析 / 投票支持意味着什么？
- 你是否以为这些数字是真实需求量或自然热度？

Clarify:

- Request / vote / support / sponsorship 都是 mock 流程，不是真实请求系统，不代表自然舆情热度。

## Core C-End Questions

- Do users understand what Sentigraph is?
- Do they understand selected sample / local demo boundaries?
- Do they mistakenly think it is real hotlist, full-web crawl, or live platform monitor?
- Can they explain PeopleCluster?
- Can they explain InfluenceCore?
- Do they understand Sandbox is local historical replay, not future prediction?
- Would they request analysis for another event?
- Would they share an event page?

## What To Watch

- The user ignores boundary copy.
- The user says “全网热榜”, “真实热度”, “官方验证”, or “预测未来”.
- The user thinks PeopleCluster means individual users.
- The user thinks InfluenceCore means influential people only.
- The user thinks vote/support count is real demand.

Record those moments in `observer_note_template.md`.
