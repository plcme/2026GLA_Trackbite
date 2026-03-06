# TrackBite 技术栈与 Setup 清单

> 团队：Developer A（Backend/Logic）+ Developer B（Frontend/Automation）
> 总冲刺：11 天 / 120–160 小时

---

## 一、Google Cloud Platform 基础设施

**1. GCP Project + Billing 启用**
- 实现什么：项目的云端根基，所有 GCP 服务的前提条件
- 为什么选：比赛强制要求后端运行在 GCP 上，且需提供部署证明截图
- Setup 位置：**浏览器 (GCP Console)**
- 耗时：A 0.5h

**2. Vertex AI API 启用**
- 实现什么：通过 API 调用 Gemini 2.0 Flash 模型
- 为什么选：比赛规定必须使用 Gemini 模型 + Google GenAI SDK，Vertex AI 是官方调用入口
- Setup 位置：**浏览器 (GCP Console)**
- 耗时：A 0.5h

**3. Cloud Run**
- 实现什么：将 FastAPI 后端容器化部署，对外提供稳定的 API 接口
- 为什么选：Serverless、自动扩容、按需计费，最适合 Hackathon 快速交付；也是评审最常见的 GCP 部署证明形式
- Setup 位置：**浏览器 (GCP Console)** 或 **终端 (gcloud CLI)**
- 耗时：A 3h

**4. Firestore（NoSQL 数据库）**
- 实现什么：存储食材库存、过期日期、用户健康档案、OCR 解析结果
- 为什么选：GCP 原生、无需运维；灵活的 JSON 结构适合食材条目这类半结构化数据；与 Cloud Run 同地域低延迟
- Setup 位置：**浏览器 (GCP Console)**
- 耗时：A 3h

**5. Cloud Storage（GCS）Bucket**
- 实现什么：临时存储用户上传的小票图片、体检报告 PDF，供 Gemini 直接读取
- 为什么选：Gemini 可直接引用 GCS URI，避免传输 base64 大文件；成本极低
- Setup 位置：**浏览器 (GCP Console)**
- 耗时：A 1h

**6. Artifact Registry + Cloud Build（可选）**
- 实现什么：自动化 Docker 镜像构建和部署流水线（IaC）
- 为什么选：比赛有 +0.2 分的"自动化部署"加分项，用 `cloudbuild.yaml` 一键部署即可满足，性价比高
- Setup 位置：**浏览器 (GCP Console)** 或 **终端 (gcloud CLI)**
- 耗时：A 2h

---

## 二、AI / Agent 核心

**7. Google GenAI SDK（Python `google-genai`）**
- 实现什么：在后端代码中调用 Gemini 2.0 Flash，处理图片输入、生成结构化输出
- 为什么选：比赛强制要求使用 Google GenAI SDK 或 ADK；Python SDK 文档最完善
- Setup 位置：**终端 (pip install)** + **代码编辑器 (Python)**
- 耗时：A 2h（安装配置）、B 1h

**8. Gemini 2.0 Flash（multimodal）**
- 实现什么：
  - 从小票/体检报告图片提取结构化食材与健康数据（OCR）
  - 分析买菜网页截图，判断下一步点击/输入操作（UI Navigator 核心）
  - 综合健康 + 日程 + 库存，生成个性化膳食建议
- 为什么选：速度快、成本低、支持图像输入，完全满足 UI Navigator 类别"截图→Gemini识别→执行动作"的强制要求
- Setup 位置：**浏览器 (Vertex AI Studio / AI Studio)** 进行 Prompt 调优
- 耗时：A 15h（Prompt 设计与调优）、B 20h（UI 导航闭环攻坚）

**9. Google Calendar API**
- 实现什么：读取用户日程（加班/健身/聚餐），作为"时间与精力"维度，决策推荐外卖/买菜/跳过
- 为什么选：规划书明确要求日程同步；Google 官方 API，与 GCP 账号天然集成，OAuth 流程成熟
- Setup 位置：**浏览器 (Google Cloud Console - APIs & Services)** 配置 OAuth 凭据
- 耗时：A 4h

---

## 三、后端框架

**10. Python 3.11+**
- 实现什么：整个后端的运行环境
- 为什么选：GenAI SDK、Playwright、Firestore SDK 均原生支持 Python
- Setup 位置：**终端 (pyenv / conda)**
- 耗时：—（环境准备）

**11. FastAPI**
- 实现什么：提供 REST API 接口，包括文件上传、决策触发、库存 CRUD、导航指令下发
- 为什么选：比 Flask 更现代，自动生成 OpenAPI 文档、原生异步支持（配合 Playwright 异步操作），类型提示友好
- Setup 位置：**终端 (pip install)**
- 耗时：A 3h

**12. Uvicorn**
- 实现什么：FastAPI 的 ASGI 生产服务器
- 为什么选：FastAPI 官方推荐，Cloud Run 容器直接用 `uvicorn main:app` 启动
- Setup 位置：**终端 (pip install)**
- 耗时：A 0.5h

**13. Pydantic v2**
- 实现什么：定义数据模型（食材条目、健康档案、膳食建议），校验 Gemini 返回的 JSON 结构
- 为什么选：FastAPI 内置，强类型约束能有效应对 Gemini 输出不稳定的情况
- Setup 位置：**终端 (pip install)**
- 耗时：A 1h

**14. python-dotenv**
- 实现什么：本地开发时用 `.env` 文件管理 GCP Key 等敏感变量
- 为什么选：安全隔离密钥，Cloud Run 上对应改用 Secret Manager
- Setup 位置：**代码编辑器 (创建 .env 文件)**
- 耗时：A 0.5h、B 0.5h

---

## 四、前端框架

**15. Next.js 14（React）**
- 实现什么：前端主框架，实现文件上传页面、库存展示、膳食建议卡片、实时导航状态展示
- 为什么选：规划书明确选型；SSR 利于演示效果，API Routes 可代理后端，部署灵活；Demo 视频中界面需要看起来专业
- Setup 位置：**终端 (npx create-next-app)**
- 耗时：B 5h

**16. TypeScript**
- 实现什么：全前端类型安全
- 为什么选：减少低级错误，在 11 天冲刺中反而节省调试时间
- Setup 位置：**终端 (npx create-next-app)**
- 耗时：B 1h（配置）

**17. Tailwind CSS**
- 实现什么：快速构建美观 UI，包括卡片、进度条、状态指示器等
- 为什么选：无需手写 CSS，组件化迅速，最适合 Hackathon 快速出视觉效果
- Setup 位置：**终端 (npx create-next-app)**
- 耗时：B 2h（配置 + 基础样式）

**18. Axios**
- 实现什么：前端调用 FastAPI 后端接口
- 为什么选：比原生 fetch 更易用，错误处理和请求拦截器方便
- Setup 位置：**终端 (npm/yarn install)**
- 耗时：B 1h

---

## 五、UI Navigator 自动化（核心攻坚）

**19. Playwright（Python async）**
- 实现什么：
  - 控制 Chromium 浏览器，在买菜/外卖网站上执行搜索、点击、加购
  - 截取当前页面截图，发给 Gemini 分析后执行下一步动作（闭环）
- 为什么选：比赛要求 UI Navigator 必须走"截图→Gemini识别→执行动作"的闭环；Playwright 比 Puppeteer 对 Python 支持更好，异步 API 与 FastAPI 天然配合
- Setup 位置：**终端 (pip install playwright)**
- 耗时：B 10h（环境配置 + 基础截图）+ 20h（UI 导航闭环攻坚，含异常处理）

**20. `playwright install chromium`**
- 实现什么：下载 Chromium 浏览器二进制，Playwright 运行必须
- 为什么选：Playwright 内置管理，Cloud Run 容器中也需在 Dockerfile 单独安装
- Setup 位置：**终端 (执行安装命令)**
- 耗时：B 1h（含 Cloud Run 容器适配）

---

## 六、容器化与部署

**21. Docker + Dockerfile**
- 实现什么：将 FastAPI + Playwright + Chromium 打包成统一可部署镜像
- 为什么选：Cloud Run 部署必须容器化；Playwright 依赖 Chromium，Dockerfile 统一管理所有系统依赖
- Setup 位置：**代码编辑器 (编写 Dockerfile)** + **终端 (Docker Desktop)**
- 耗时：A 3h

**22. `cloudbuild.yaml`**
- 实现什么：自动化构建 Docker 镜像并推送到 Cloud Run
- 为什么选：满足比赛 +0.2 分"自动化部署"加分项，1h 成本拿到额外分数
- Setup 位置：**代码编辑器 (编写 YAML)**
- 耗时：A 1h

---

## 七、开发工具与比赛交付

**23. GitHub（Public Repo）**
- 实现什么：代码版本管理；比赛提交必须提供公开代码库链接，评审会看 commit 历史
- 为什么选：比赛强制要求
- Setup 位置：**浏览器 (GitHub.com)** + **终端 (git CLI)**
- 耗时：A 0.5h、B 0.5h（初始化配置）

**24. `README.md`（Spin-up 指南）**
- 实现什么：step-by-step 本地运行/云端部署文档，环境变量配置说明——评审打分重要参考
- 为什么选：比赛明确要求有可复现的部署文档，即使评审不运行代码，文档本身也是可信度的体现
- Setup 位置：**代码编辑器**
- 耗时：A 5h

**25. 架构图（draw.io / Excalidraw）**
- 实现什么：可视化展示 Gemini 如何连接后端、Firestore、Calendar、Playwright 的完整数据流
- 为什么选：比赛提交必须包含架构图，属于 Demo & Presentation 评分项（占总分 30%）的核心材料
- Setup 位置：**浏览器 (设计工具)**
- 耗时：A 3h

**26. 演示视频（OBS/QuickTime + 剪辑工具）**
- 实现什么：4 分钟内展示完整闭环：上传小票 → OCR 解析 → 膳食决策 → Playwright 自动加购，需英文字幕
- 为什么选：比赛强制要求，且"The Live Factor"是 Demo & Presentation 评分的核心，必须展示真实软件运行而非 mockup
- Setup 位置：**录屏剪辑软件**
- 耗时：B 10h（录制 + 剪辑 + 英文字幕）

---

## 时间汇总

**Developer A（Backend/Logic）总计：~52h**
- GCP 基础设施：~10h
- AI/Agent SDK + Prompt 设计：~21h
- 后端框架搭建：~8h
- 容器化与部署：~4h
- 文档与架构图：~9h

**Developer B（Frontend/Automation）总计：~72h**
- AI/Agent SDK 配置：~1h
- 前端框架搭建：~9h
- Playwright UI 导航（核心攻坚）：~31h
- 开发工具配置：~0.5h
- 演示视频制作：~10h

> B 的负担明显重于 A，主要集中在 Playwright + Gemini 导航闭环（约 31h）。建议 Day 3–5 阶段 A 完成 Calendar/Firestore 集成后，抽时间协助 B 调试 UI 导航逻辑。
