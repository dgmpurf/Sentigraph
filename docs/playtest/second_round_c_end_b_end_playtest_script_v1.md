# Second-Round C-End / B-End Playtest Script v1

Status: docs-only script. This script does not implement runtime behavior, data collection, report generation, Response Strategy Lab runtime, live APIs, or platform actions.

## 1. Short Intro Spoken By Tester

Use this before screen sharing:

> 今天想请你看一个本地演示版本。它展示的是公共事件如何被整理成事件页、样本说明、生态沙盒和报告样例。请先按直觉说你看懂了什么、哪里困惑。过程中有些页面是 mock 或 selected public sample，我会先让你自己反应，再补充边界说明。

If recording:

> 这次只记录产品反馈，不记录私人账号、私密数据、平台登录信息或个人敏感信息。你可以随时让我暂停。

## 2. C-End Guided Route Script

### Step 1: Open `/#/demo`

What to click:

- Open the guided demo page.
- Let the participant scan for 10-20 seconds.

Neutral prompt:

- "你觉得这个页面在引导你做什么？"
- "你会先点哪里？"

Do not say yet:

- "这是本地 demo，不是全网系统。"

Clarify after reaction:

- "这里是本地 guided demo，不是线上公共平台入口。"
- "页面里的搜索或筛选如果出现，仅筛选本地 demo 事件，不进行全网搜索或抓取。"

### Step 2: Open `/#/public-events`

What to click:

- Enter Event Plaza.
- Let the participant identify event cards.

Neutral prompt:

- "你觉得这些事件卡代表什么？"
- "你会打开哪个事件？为什么？"

Clarify after reaction:

- "这里是公共事件入口原型，不是实时全网事件库。"
- "热度或争议字段如果标注为 mock，就不是自然公共舆情热度。"

### Step 3: Open `/#/public-events?guided=1`

What to click:

- Show guided Event Plaza if available.

Neutral prompt:

- "有 guided 参数以后，你觉得页面更清楚了吗？"
- "你知道下一步该去哪里吗？"

Clarify after reaction:

- "这个引导是为了降低首次使用门槛，不代表平台已进入生产运营。"

### Step 4: Open `/#/public-events/helldivers-psn`

What to click:

- Open Helldivers detail page.
- Pause on sample boundary or event summary if visible.

Neutral prompt:

- "你觉得这页是在讲事件事实、样本摘要，还是分析结论？"
- "你能看出样本边界吗？"

Clarify after reaction:

- "Helldivers 是 selected public sample。"
- "它不是 full-web coverage、不是 full-platform coverage、不是 full-thread coverage。"
- "它不是 official verification，也不是 causal proof。"

### Step 5: Open `/#/public-events/donglu-sunjihai-youth-football`

What to click:

- Open Dong Lu / Sun Jihai youth football event detail.

Neutral prompt:

- "换成中文体育事件后，你理解这个产品的用途有没有变化？"
- "你觉得这页适合分享给普通用户，还是更适合专业人员？"

Clarify after reaction:

- "这个样本是 controlled candidate public sample，不是官方验证，也不是完整复盘。"
- "它不能判断谁对谁错，只能帮助结构化理解公开讨论样本。"

### Step 6: Open `/#/opinion-ecosystem`

What to click:

- Enter Opinion Ecosystem Sandbox.
- Switch to V2 ecology view if needed.

Neutral prompt:

- "先不解释，你觉得这些图形分别代表什么？"
- "你觉得小球是什么？大一点或核心节点是什么？"

Clarify after reaction:

- "PeopleCluster 小球代表匿名群体簇，不代表真实个人。"
- "InfluenceCore 代表内容、叙事、官方、媒体、meme 等核心，不是人。"
- "EchoBox 是讨论语境容器和压力空间的可视化。"

### Step 7: Open `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`

What to click:

- Switch to the Chinese event sample if supported by route.
- Move through visible timeline or scenario states.

Neutral prompt:

- "换成这个样本后，图是不是更容易理解？"
- "你觉得哪些指标值得信任，哪些需要解释？"

Clarify after reaction:

- "这些指标是本地 demo / heuristic / fixture interpretation，不是科学校准后的生产指标。"
- "Response Strategy Lab 如果出现，只是 planned-only 或说明，不是 active runtime。"

### Step 8: Open `/#/public-events/request`

What to click:

- Open request / vote mock flow.

Neutral prompt:

- "你觉得这个请求/投票入口会让你做什么？"
- "你会愿意请求另一个事件吗？"

Clarify after reaction:

- "Request / vote 是 mock flow，不代表真实平台热度。"
- "它不触发真实分析任务、真实平台动作、真实 API 或真实 LLM。"

## 3. B-End Professional Route Script

### Step 1: Start At `/#/demo`

Neutral prompt:

- "如果你是品牌、公关、社区运营或内容团队，你觉得这个入口是否能解释产品能力？"
- "哪里像产品，哪里还像 demo？"

Clarify after reaction:

- "这轮主要测理解和价值，不测生产接入。"

### Step 2: Open `/#/public-events/donglu-sunjihai-youth-football`

Neutral prompt:

- "从专业视角，这个事件页提供了哪些可用于汇报的上下文？"
- "你会希望补哪些来源、证据或审核状态？"

Clarify after reaction:

- "样本不是完整覆盖，也不是官方验证。"
- "专业场景要看 evidence coverage、trust、review、dedup、audit，而不是只看结论。"

### Step 3: Open `/#/opinion-ecosystem?sample=donglu-sunjihai-youth-football`

Neutral prompt:

- "这张生态图是否帮助你解释事件结构？"
- "你能不能把 PeopleCluster 和 InfluenceCore 讲给同事听？"

Clarify after reaction:

- "PeopleCluster 是匿名群体簇，不能用于个人画像或定向影响。"
- "InfluenceCore 是叙事或内容核心，不能当成真实个人。"

### Step 4: Open `/#/reports/donglu-sunjihai-youth-football-sample`

Neutral prompt:

- "如果这是客户或管理层汇报样例，你最先看哪一段？"
- "哪些段落让你觉得有决策价值？哪些段落需要更强证据？"

Clarify after reaction:

- "这是 fixed sample report，不是 dynamic production report。"
- "它不代表 PDF / PPT / client delivery runtime 已经上线。"
- "高影响结论和建议动作需要人工、法务、政策或客户侧复核。"

### Step 5: Open `/#/reports/helldivers-psn-sample`

Neutral prompt:

- "换成游戏社区事件后，这个报告结构是否仍然有用？"
- "你觉得报告模板适合哪些行业？"

Clarify after reaction:

- "不同事件样本可验证结构复用性，但不证明模型已经生产校准。"

### Step 6: Open `/#/public-events/request`

Neutral prompt:

- "你是否理解 C-end 请求/投票和 B-end 咨询之间的关系？"
- "如果你是品牌/MCN/运营方，你会希望怎样接入？"

Clarify after reaction:

- "这只是 mock request and vote flow，不创建生产 case、生产 review queue、生产 dedup 或真实分析任务。"

### Step 7: Optional `/#/external-collector`

Use only if the reviewer asks where selected samples come from.

Neutral prompt:

- "你看到这个桥接页后，是否更信任样本来源说明？"
- "是否仍然会误以为 Sentigraph 内置了爬虫？"

Clarify after reaction:

- "External Collector Bridge 只说明本地 Evidence Export package 的来源与校验状态。"
- "它不运行 crawler job、不搜索全网、不抓取 URL、不调用真实 API。"

## 4. Boundary Explanations To Use After First Reaction

Use short explanations:

- "当前是 local demo / selected sample / mock where labeled。"
- "这不是 full-web coverage。"
- "这不是 live platform crawling。"
- "这不是 causal proof。"
- "这不是 real public event platform yet。"
- "PeopleCluster 是 anonymous groups/clusters，不是真实个人。"
- "InfluenceCore 是 content / narrative / official / media / meme core，不是小球、不是人。"
- "B-end report sample 是 fixed sample report，不是 dynamic production report。"
- "Response Strategy Lab 是 planned-only，不是 active runtime。"

## 5. Debrief Questions

Ask these after the route:

1. 你用一句话描述 Sentigraph 是什么？
2. 你觉得它现在是线上产品、原型、报告工具，还是分析平台？
3. 哪个页面最容易懂？
4. 哪个页面最容易误解？
5. 你是否误以为它在抓取全网或实时平台？
6. 你是否理解 selected sample 的限制？
7. 你是否理解 PeopleCluster 和 InfluenceCore 的区别？
8. 你是否相信 B-end report sample 对专业团队有用？
9. 你愿意分享一个事件页吗？
10. 你愿意请求另一个事件分析吗？
11. 如果你是专业客户，你会愿意进一步沟通吗？
12. 你最希望下一版先改什么？

## 6. What To Avoid Saying

Avoid:

- "我们已经全网覆盖。"
- "这是实时爬虫结果。"
- "这些是官方验证数据。"
- "这证明了因果关系。"
- "这些小球是真实用户。"
- "InfluenceCore 是大 V 或具体人。"
- "报告是生产级动态生成。"
- "Response Strategy Lab 已经可以执行策略。"
- "投票是真实热度。"
- "这个系统能自动做公关动作。"
- "我们已经接入 Douyin / Bilibili / RSS / GDELT / vendor / real LLM。"

## 7. Tester Notes

Keep tone neutral:

- Do not defend the product during the first reaction.
- Do not correct every misunderstanding immediately.
- Mark exact words the participant uses.
- Ask "what made you think that?" when they misunderstand.
- Use the feedback form after the route, not during every page.

The goal is to find confusion, not to win the demo.
