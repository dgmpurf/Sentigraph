# Sentigraph 舆情图谱系统

Sentigraph 是一个 AI-powered public opinion analysis and risk monitoring system，用于围绕关键词监测公开舆情、分析情绪与话题、识别重复话术/疑似水军信号、计算舆情风险，并在桌面端仪表盘中展示图表、传播图谱和结构化舆情报告。

当前项目处于 **desktop-first Web MVP** 阶段。系统优先使用本地 mock/offline 数据和确定性的规则/模板逻辑，暂不依赖真实爬虫、真实平台 API、OpenAI API 或任何外部 LLM API。

本项目还不是生产系统。

## 1. Project Overview

- 产品形态：PC/浏览器端深色科幻风格舆情分析仪表盘。
- 当前定位：mock-first MVP，先验证完整产品链路和前后端数据契约。
- 当前数据：本地 `mock_data/` 和后端 deterministic mock pipeline。
- 当前报告：后端模板化中文舆情报告，前端默认以中文展示。
- 当前安全边界：不实现登录绕过、验证码绕过、反爬规避、私有数据采集或密钥硬编码。

核心链路：

```text
关键词输入 -> 平台选择 -> mock 数据 -> 清洗/去重 -> 情绪/话题/水军/风险分析 -> 报告生成 -> 桌面仪表盘展示
```

## 2. Current MVP Status

当前已经可用：

- 桌面优先 Web dashboard，目标布局为 1440px PC/browser dashboard。
- FastAPI 后端 mock pipeline。
- React + Vite 前端仪表盘。
- 平台注册表 `GET /api/v1/platforms`。
- mock 关键词扩展、mock crawl task、mock analysis flow。
- 文本清洗、重复检测、用户聚合。
- deterministic mock sentiment/topic/bot/risk analysis services。
- 可视化数据构建，包括情绪趋势、风险雷达、热力图、话题聚类、传播图谱、疑似水军影响。
- 模板化 summary/recommendation/report builder。
- normalized Chinese public opinion report API。
- Summary Report 和 Analysis Result 页面已接入后端中文结构化报告。
- 轻量分析案例管理：可创建本地 mock 案例、运行 V1.5 mock 分析、查看案例列表并导出 Markdown 报告。
- backend pytest 与 frontend build 已在本地验证通过。

当前没有实现：

- 真实平台 API 调用。
- 真实爬虫。
- OpenAI 或外部 LLM 调用。
- MongoDB/Redis 持久化。
- 登录、鉴权、用户系统。
- 生产级部署和监控。

## 3. Features

### MVP Available Features

- 关键词输入与 mock 关键词扩展。
- mock 平台选择与 mock 分析流程。
- 本地内存型 analysis case 管理与 Markdown 报告复制/下载。
- 后端平台 registry，区分 mock-selectable、official API planned、crawler-later、optional future。
- 后端 deterministic mock analysis pipeline。
- 情绪分析、话题聚类、重复话术/疑似水军信号、风险评分。
- Dashboard、Keyword Search、Analysis Result、Propagation Graph、Risk Monitor、Summary Report 页面。
- ECharts 图表：情绪趋势、风险雷达、话题图、平台热力、传播图谱。
- 中文结构化舆情报告：
  - 舆情总览
  - 核心发现
  - 主要风险因素
  - 高风险话题
  - 代表性评论
  - 疑似水军/重复话术信号
  - 建议行动
  - 建议公开回应文案
- 建议公开回应文案复制按钮。

### Planned Features

- 更完整的浏览器端 smoke test。
- 后端响应中以兼容方式加入 `risk_model_version` 和中文风险等级展示字段。
- 更细的可视化交互和报告导出体验。
- 增量监控、告警、趋势变化检测。
- 真实平台 adapter 接口设计。
- MongoDB/Redis/Celery 或调度任务支持。

### Future Advanced Features

- Reddit real adapter。
- 中国平台官方 API 集成。
- crawler-later 平台的公开页面 parser 和 selector profile。
- V2 topic-cluster dynamic risk model。
- 历史 topic baseline、影响力图谱、可信度模型。
- 可选 LLM 辅助 topic labeling、风险解释和响应草稿，但必须经过严格 JSON/schema 校验。

## 4. Platform Roadmap

### MVP Mock-selectable Platforms

这些平台当前只用于离线 mock 分析，不会触发真实 API 调用或真实爬虫：

- Reddit
- Weibo
- Bilibili
- Douyin
- Kuaishou
- Xiaohongshu
- Zhihu
- Douban
- Toutiao

Reddit 保留在项目中，当前可 mock-selectable，未来可作为 real adapter candidate。

### Official API Planned

后续优先研究官方 API、权限、配额和合规要求：

- Weibo
- Bilibili
- Douyin
- Kuaishou
- Xiaohongshu
- Zhihu
- Douban
- Toutiao

这些平台当前只支持 mock workflow，不代表真实集成已经完成。

### Future Crawler-later

这些平台未来可考虑基于公开页面 parser 和 selector profile 实现，但当前不可用于真实采集：

- Hupu
- Baidu Tieba
- Tianya
- NGA
- Maimai
- The Paper / Pengpai News
- Jiemian News

未来 crawler-later 工作必须只处理公开页面，不能绕过登录、验证码、付费墙、反爬系统或访问私有数据。

### Disabled or Optional Future

- YouTube

YouTube 不是当前 MVP active platform，不在当前 roadmap 中优先实现，只作为 optional future source 保留。

## 5. Architecture

当前架构是前后端分离的 mock-first Web MVP：

```text
frontend/
  React + Vite desktop dashboard
  Ant Design UI
  ECharts visualizations
  Axios API client

backend/
  FastAPI API routes
  Pydantic schemas
  deterministic mock services
  preprocessing / NLP / bot detection / scoring / visualization / report builder

mock_data/
  local raw comments and pipeline fixtures

docs/
  API contract, data schema, platform roadmap, risk algorithm design, progress log
```

分析流：

```text
keyword input
  -> platform selection
  -> mock data
  -> preprocessing
  -> duplicate detection
  -> sentiment/topic/bot/risk analysis
  -> visualization response
  -> template-based report builder
  -> desktop dashboard
```

## 6. Risk Model

当前 active model：

```text
v1_static_mvp
```

V1 当前用于 MVP 静态评分，结合负面情绪、负面强度、疑似水军影响、传播速度、争议程度和趋势变化等 mock pipeline 信号，输出项目级 `risk_score` 与 `risk_level`。

未来模型：

```text
v2_topic_dynamic_planned
```

V2 设计已在 `docs/algorithm_design.md` 和 `docs/risk_model_roadmap.md` 中记录。核心方向是按 topic cluster 与 time window 计算动态风险，并区分：

- real_crisis_risk
- manipulation_risk

V2 目前只是文档和占位设计，尚未完整实现，也未接管当前 scoring behavior。

Current mock pipeline/report responses also expose the implemented V1.5 topic-risk layer:

```text
v1_5_topic_risk_mvp
```

V1.5 is deterministic and offline. It adds `topic_risks`, `top_risk_topics`, `overall_risk`, `real_crisis_risk`, and `manipulation_risk` while keeping the old V1 `risk_score` and `risk_level` fields backward-compatible.

## 7. Tech Stack

Backend:

- Python 3.10+
- FastAPI
- Pydantic
- Pytest
- MongoDB/Redis/Celery or scheduler support planned for future phases

Frontend:

- React
- Vite
- Ant Design
- ECharts
- Framer Motion
- Axios

## 8. Local Development on Windows

以下命令使用 Windows CMD 写法。请在本机确认 Python 3.10+、Node.js 和 npm 已安装。

### Backend

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest
cd backend
uvicorn app.main:app --reload
```

后端默认地址：

```text
http://127.0.0.1:8000
```

健康检查：

```text
http://127.0.0.1:8000/api/v1/health
```

API docs：

```text
http://127.0.0.1:8000/docs
```

### Frontend

另开一个终端：

```cmd
cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\frontend"
npm install
npm run dev
npm run build
```

开发服务器：

```text
http://127.0.0.1:5173
```

Vite 开发环境会把 `/api` 请求代理到后端 `http://127.0.0.1:8000`。

### Root Helper Scripts

也可以从仓库根目录使用：

```cmd
npm run backend:test
npm run backend:dev
npm run frontend:dev
npm run frontend:build
```

## 9. API Overview

Base path:

```text
/api/v1
```

主要已实现 endpoints：

- `GET /api/v1/health`
- `GET /api/v1/platforms`
- `POST /api/v1/keywords/expand`
- `POST /api/v1/crawl/start`
- `POST /api/v1/analysis/run`
- `POST /api/v1/visualization/data`
- `POST /api/v1/summary/generate`
- `POST /api/v1/recommendation/generate`
- `GET /api/v1/cases`
- `POST /api/v1/cases`
- `GET /api/v1/cases/{case_id}`
- `POST /api/v1/cases/{case_id}/run`
- `GET /api/v1/cases/{case_id}/report/markdown`

其他已实现 mock endpoints：

- `GET /api/v1/analysis/{project_id}`
- `GET /api/v1/propagation/{project_id}`
- `GET /api/v1/alerts/{project_id}`

完整契约见 `docs/api_contract.md`。

## 10. Important Constraints

- mock-first：当前优先使用 mock/offline data。
- no real crawlers yet。
- no real platform APIs yet。
- no OpenAI API or external LLM API required。
- no login bypass。
- no captcha bypass。
- no anti-bot evasion。
- no private data collection。
- no hardcoded secrets。
- MongoDB document keys must be strings。
- 前端不要直接渲染 JavaScript object。
- 代表性评论保持原语言，不自动翻译。
- 前端报告默认中文展示，默认请求 `report_language: "zh-CN"`。

## 11. Roadmap

- MVP 0: repository skeleton and mock dashboard。
- MVP 1: mock pipeline and visualization。
- MVP 2: structured report builder。
- MVP 3: frontend report pages。
- MVP 4: visualization refinement。
- MVP 5: Reddit real adapter。
- MVP 6: official API integrations。
- MVP 7: crawler-later platforms。
- MVP 8: advanced V2 dynamic risk model。

## 12. Repository Structure

```text
Sentigraph/
  backend/
    app/
      api/
      schemas/
      services/
      tests/
    requirements.txt
  frontend/
    src/
      api/
      components/
      pages/
      styles/
      utils/
    package.json
  docs/
    api_contract.md
    data_schema.md
    development_plan.md
    platform_sources.md
    algorithm_design.md
    risk_model_roadmap.md
    progress.md
  mock_data/
  AGENTS.md
  README.md
  requirements.txt
  package.json
```

## 13. Development Notes for Codex

- 每次开始新任务前，先读 `AGENTS.md` 和 `docs/progress.md`。
- 涉及 API、schema、frontend 数据映射时，对照 `docs/api_contract.md` 和 `docs/data_schema.md`。
- 每个 major Codex task 后更新 `docs/progress.md`，除非任务明确要求只改某个文件。
- 保持 mock-first，不要提前接入真实爬虫、真实平台 API 或外部 LLM。
- 保持 backend route thin，把业务逻辑放在 services。
- 保持 frontend API 调用集中在 `frontend/src/api`。
- 不要声称生产可用，除非后续完成真实数据、鉴权、持久化、部署和合规审查。
