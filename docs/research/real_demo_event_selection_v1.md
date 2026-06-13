# Sentigraph Real Demo Event Selection v1

**更新时间**：2026-06-13  
**用途**：为 Sentigraph Phase 4 真实 demo 选择低风险、可解释、可用公开证据整理的数据事件。  
**性质**：research/design 文档，不代表已接入真实平台 API，不代表已完成真实数据驱动 simulation。

---

## 结论

第一版真实 demo 推荐选择：

> **Helldivers 2 / 绝地潜兵 2：PSN 账号绑定争议**

这是一个游戏社区事件，适合展示 Sentigraph 的：

```text
Influence Core / 观念核心
EchoBox / 回音壁容器
People Cluster / 人群簇
Camp Dynamics / 阵营迁移
Deconstruction Core / 二次解构
Response Tempo / 处理节奏
Reputation Memory / 声誉残留
```

它适合做 **C 端公开展示 demo + B 端公关分析样板**。

---

## 为什么选择 Helldivers 2 PSN 事件

### 1. 它是游戏社区争议，不是高敏社会事件

它围绕 PC/Steam 玩家是否必须绑定 PlayStation Network 账号展开，属于产品策略、平台账号、玩家权益、区域可用性和沟通节奏争议。

这类事件适合 Sentigraph 第一版真实 demo，因为：

```text
低于政治/司法/社会高敏事件风险
有清晰的正 / 中 / 反人群
有官方公告、玩家社区、媒体报道、创作者评论等多种 Influence Core
有回音壁，也有破圈风险
有完整生命周期和后续符号化处理
```

### 2. 它有明确事件链路

可抽象为：

```text
官方账号绑定公告
→ 玩家疑虑和反对
→ Steam / Reddit / YouTube / 新闻扩散
→ 负面评价集中爆发
→ 官方撤回账号绑定要求
→ 社区转向、部分好评恢复
→ 后续用 review bomb cape 纪念 / 梗化
```

### 3. 它非常适合 EchoBox 模型

可建模 EchoBox：

```text
Steam 玩家回音壁
Reddit 玩家社区
YouTube 评论区
游戏媒体报道区
PlayStation / Arrowhead 官方回应区
```

这些 EchoBox 可以互相连接，也可展示：

```text
高热封闭型
高渗透破圈型
官方回应触发型
社区解构型
```

### 4. 它非常适合 Influence Core

可建模 Influence Core：

```text
官方账号绑定公告
PlayStation 撤回声明
玩家负面评价与 Steam review graph
社区“清理差评 / 改回好评”叙事
创作者分析视频
后续 review bomb cape / 纪念披风
```

### 5. 它适合 Deconstruction Core / Reputation Memory

后续纪念披风是一个很好的“二次解构 / 符号降压 / 社区共创”案例：

```text
原始冲突：PSN 绑定要求引发反弹
后续符号：review bomb graph 被做成纪念披风
潜在含义：冲突记忆被转译成社区内部符号
```

这很适合演示 Sentigraph 的“声量下降不等于事件消失；事件可能转为长期符号或声誉记忆”。

---

## 不作为真实 live API demo

当前 Sentigraph 边界不变：

```text
不做全网爬虫
不抓 Steam / Reddit / YouTube 网页
不调用真实 search API
不调用真实 LLM
不接 MediaCrawler / OpenClaw 生产采集
不把 Search/RSS/GDELT mock/static 说成 live provider
```

真实 demo 的数据建议使用：

```text
公开资料手动整理成 CSV/Excel
Manual URL evidence
可选 YouTube official API，只限本地 .env 启用并符合 YouTube API 条款
公开媒体报道和官方公告作为手动证据
```

---

## Demo 数据采样建议

### Evidence roots / Influence Core roots

建议收集 8–12 个 root-level evidence：

```text
1. 官方账号绑定公告
2. 撤回账号绑定要求的官方更新
3. 游戏媒体报道：事件经过
4. 游戏媒体报道：review bombing / 评价变化
5. YouTube 创作者分析视频 A
6. YouTube 创作者分析视频 B
7. Reddit / Steam 社区讨论样本入口
8. 后续 review bomb cape / 社区符号化报道
```

### 评论样本

建议手动整理 300–800 条评论样本，字段：

```text
platform
source_url
root_id
parent_id
comment_text
created_at
like_count
reply_count
stance_label_manual_optional
topic_label_manual_optional
trust_label
review_status
duplicate_group_id
```

第一版真实 demo 不需要追求全量，只需要清楚标注：

```text
基于已导入/可用证据
不代表全网全量覆盖
不代表因果确定
```

---

## 可展示的人群簇

PeopleCluster 示例：

```text
受影响地区玩家反对群体
隐私/账号绑定反对群体
“创建账号很简单”温和支持群体
索尼/平台策略批评群体
Arrowhead 同情/支持群体
证据敏感中立群体
疲劳围观群体
社区梗化参与群体
```

---

## 可展示的处理节奏

ResponseTempo 示例：

```text
早期：应更早说明 PSN 绑定必要性、地区可用性和玩家影响。
峰值期：优先补充事实说明和责任边界，避免强硬表达。
撤回后：中立者和温和反对者存在中立化窗口。
后期：社区已出现符号化 / 解构空间，可作为声誉记忆监测案例。
长期：review bomb cape 代表事件没有消失，而是转为社区符号。
```

---

## 备选事件

### 备选 A：Escape from Tarkov / Unheard Edition 争议

优点：

```text
付费版本、PvE 模式、玩家权益和承诺落差明显
适合 B 端公关分析
反方核心和官方回应都很清晰
```

缺点：

```text
争议商业味更重
游戏社区相对硬核
不如 Helldivers 2 适合 C 端展示
```

### 备选 B：Ready or Not 内容调整 / Console launch 争议

优点：

```text
适合展示不同平台受众、商业取舍、老玩家与新市场冲突
```

缺点：

```text
涉及内容审查 / censor 语境，解释风险略高
不适合第一版公开 demo
```

---

## 推荐排序

```text
1. Helldivers 2 PSN 账号绑定争议
2. Escape from Tarkov Unheard Edition 争议
3. Ready or Not 内容调整 / console launch 争议
```

---

## 后续落地路线

```text
Phase 4A：确定真实 demo 事件与数据采样范围
Phase 4B：创建 CSV/Excel 样本模板
Phase 4C：整理 300–800 条真实公开评论/证据样本
Phase 4D：导入 Sentigraph Evidence Layer
Phase 4E：手动或 fixture 方式映射到 Opinion Ecosystem Sandbox
Phase 4F：生成 C 端公开事件页 + B 端报告样例
```

---

## 参考来源

- Steam News: HELLDIVERS™ 2 Account Linking Update  
  https://store.steampowered.com/news/app/553850/view/4196868529806518741
- Game World Observer: Helldivers 2 players prove review bombing can lead to positive change  
  https://gameworldobserver.com/2024/05/06/helldivers-2-psn-linking-removed-review-bombing-positive
- GamesRadar+: Helldivers 2 review bomb cape  
  https://www.gamesradar.com/games/third-person-shooter/helldivers-2-finally-gets-its-review-bomb-cape-to-celebrate-your-unquestioning-commitment-to-the-defense-of-managed-democracy/
- Hitmarker: Escape from Tarkov dev apologizes to players and changes exclusive PvE mode plans  
  https://hitmarker.net/news/escape-from-tarkov-dev-apologizes-to-players-and-changes-exclusive-pve-mode-plans-903478
- PC Gamer: Ready or Not console launch / content changes and backlash  
  https://www.pcgamer.com/games/fps/ready-or-not-has-sold-1-million-units-on-console-10-times-faster-than-what-was-achieved-on-pc-proving-that-the-censorship-was-worth-it/
