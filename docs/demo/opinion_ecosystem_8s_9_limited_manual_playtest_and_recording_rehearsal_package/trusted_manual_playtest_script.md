# Trusted Manual Playtest Script

## A. Opening Instructions To Tester

Use this only with a known trusted tester.

Opening:

> 我想请你体验一个本地 demo。请你边点边说你自然理解到的内容：它在做什么、哪里可信、哪里让你误解。请不要输入任何私人或敏感真实数据，也不要登录个人账号。本次不会抓取实时数据、不会调用真实 API、不会连接 private collector。

## B. Think-aloud Prompts

Ask the tester to speak aloud:

- what they think each page is for
- what they expect after clicking a button
- where wording feels too strong
- where boundaries are visible or invisible
- whether generated-run output feels clearer than static explanation

## C. Questions Before Explanation

- What do you think this product does?
- Do you think it is live crawling?
- Do you think this is full-web coverage?
- Do you think the Dong/Sun sample is official truth?
- What do you think the small balls represent?
- What do you think InfluenceCore means?
- What do you think generated-run means?
- Would you expect it to post, send, publish, or execute anything?

## D. Questions After Explanation

- Did selected sample only make sense?
- Did you understand that this is not official verification?
- Did you understand that this is not prediction or causal proof?
- Did generated-run display help compared with static explanation?
- Did the B-end report sample feel useful?
- What was confusing?
- What would you expect next?
- Would you ask for another event analysis?
- Would you share an event page with this boundary language?

## E. Misunderstanding Probes

Probe gently:

- “If I said this is full-web coverage, would that sound right?”
- “If I said the generated run is a production score, would that sound right?”
- “If I said PeopleCluster balls are real users, would that sound right?”
- “If I said ResponseStrategyComparison auto-generates a public reply, would that sound right?”

Correct answer:

- no live crawling
- no full-web coverage
- no official truth
- no production score
- PeopleCluster is anonymous aggregate group / behavioral proxy
- ResponseStrategyComparison is human-review-only

## F. Prohibited Tester Actions

- do not enter private/sensitive real data
- do not ask the operator to crawl live data during this run
- do not paste secrets
- do not log into personal accounts
- do not connect private collector
- do not provide API keys, tokens, cookies, sessions, or browser profile paths
- do not ask for publish / send / post / execute action

## G. Stop Conditions

Stop immediately if:

- tester thinks the system is live crawling and cannot be corrected
- tester thinks generated run is official truth
- tester thinks small balls are real people
- UI shows 500 / ErrorBoundary / `undefined` / `NaN` / `[object Object]`
- publish / send / post / execute CTA appears
- generated public response text appears
- raw author identifiers appear
- secrets, `.env`, API keys, tokens, cookies, sessions, or browser profile paths are visible
- backend or frontend crashes
- private collector path or real exchange dir appears
