# TrackBite 技术栈与 Setup 清单

> 团队：2 名 Agent Beginner (Developer A = Backend/Logic，Developer B = Frontend/Automation)
> 总冲刺：11 天 / 120–160 小时

---

## 一、Google Cloud Platform (GCP) 基础设施

| 技术 / Setup | 实现的功能 | 为什么选择 | Dev A 耗时 | Dev B 耗时 |
|---|---|---|---|---|
| **GCP Project + Billing 启用** | 项目的云端根基，所有 GCP 服务的前提 | 比赛强制要求在 GCP 上运行，且需提供部署证明截图 | 0.5h | — |
| **Vertex AI API 启用** | 调用 Gemini 2.0 Flash 模型做多模态推理（OCR、UI 识别、决策） | 比赛规定必须用 Gemini 模型 + Google GenAI SDK，Vertex AI 是官方入口 | 0.5h | — |
| **Cloud Run** | 将 FastAPI 后端容器化部署，对外提供 API 接口 | Serverless、自动扩容、按需计费，最适合 Hackathon 快速交付；也是评审最常见的 GCP 部署证明形式 | 3h | — |
| **Firestore (NoSQL 数据库)** | 存储食材库存、过期日期、用户健康档案、解析结果 | GCP 原生、无需运维、与 Cloud Run 同地域低延迟；灵活 JSON 结构适合食材条目这种半结构化数据 | 3h | — |
| **Cloud Storage (GCS) Bucket** | 临时存储用户上传的小票图片、体检报告 PDF，供 Gemini 读取 | Gemini 可直接引用 GCS URI，避免 base64 大文件传输；成本极低 | 1h | — |
| **Artifact Registry + Cloud Build (可选)** | 自动化 Docker 镜像构建和部署流水线 | 比赛有 +0.2 分的"自动化部署"加分项，用 `cloudbuild.yaml` 一键部署即可满足 | 2h | — |

---

## 二、AI / Agent 核心

| 技术 / Setup | 实现的功能 | 为什么选择 | Dev A 耗时 | Dev B 耗时 |
|---|---|---|---|---|
| **Google GenAI SDK (Python `google-genai`)** | 调用 Gemini 2.0 Flash：OCR 解析小票/报告、分析截图、生成膳食建议 | 比赛强制要求使用 Google GenAI SDK 或 ADK；Python SDK 文档最完善 | 2h | 1h |
| **Gemini 2.0 Flash (multimodal)** | ① 从小票/报告图片提取结构化食材/健康数据（OCR） ② 分析买菜网页截图、判断下一步操作（UI Navigator 核心） ③ 综合健康+日程+库存生成膳食建议文本 | 速度快、成本低、支持图像输入，完全满足 UI Navigator 类别的"视觉截图→执行动作"强制要求 | 15h (Prompt 设计) | 20h (UI 导航闭环) |
| **Google Calendar API** | 读取用户日程（加班/健身/聚餐），作为"时间与精力"维度输入，决定推荐外卖/买菜/跳过 | 比赛和规划书明确要求日程同步；Google 官方 API，与 GCP 账号天然集成，OAuth 流程成熟 | 4h | — |

---

## 三、后端框架

| 技术 / Setup | 实现的功能 | 为什么选择 | Dev A 耗时 | Dev B 耗时 |
|---|---|---|---|---|
| **Python 3.11+** | 整个后端运行环境 | GenAI SDK、Playwright、Firestore SDK 均原生支持 Python；团队熟悉度高 | — (环境) | — |
| **FastAPI** | 提供 REST API 接口：文件上传、决策触发、库存 CRUD、导航指令下发 | 比规划书提到的 Flask 更现代：自动生成 OpenAPI 文档、异步支持好（配合 Playwright 异步操作）、类型提示友好 | 3h | — |
| **Uvicorn** | FastAPI 的 ASGI 服务器，生产运行 | FastAPI 官方推荐，Cloud Run 容器直接用 `uvicorn main:app` 启动 | 0.5h | — |
| **Pydantic v2** | 定义数据模型（食材条目、健康档案、膳食建议结构）、校验 Gemini 输出 JSON | FastAPI 内置，强类型约束避免 Gemini 返回结构不稳定 | 1h | — |
| **python-dotenv** | 管理 GCP Key、API Key 等环境变量，本地开发 `.env` 文件 | 安全隔离密钥，Cloud Run 上改用 Secret Manager | 0.5h | 0.5h |

---

## 四、前端框架

| 技术 / Setup | 实现的功能 | 为什么选择 | Dev A 耗时 | Dev B 耗时 |
|---|---|---|---|---|
| **Next.js 14 (React)** | 前端主框架：文件上传页面、库存展示、膳食建议卡片、实时导航状态展示 | 规划书明确选型；SSR 利于 SEO、API Routes 可代理后端、部署 Vercel/Cloud Run 均可；比赛演示 Demo 需要看起来专业 | — | 5h |
| **TypeScript** | 全前端类型安全 | 减少低级错误，在 11 天冲刺中反而节省调试时间 | — | 1h (配置) |
| **Tailwind CSS** | 快速构建美观 UI（卡片、进度条、状态指示器） | 无需手写 CSS，组件化迅速，适合 Hackathon 快速出样式 | — | 2h (配置+基础样式) |
| **Axios** | 前端调用 FastAPI 后端接口 | 比原生 fetch 更易用，错误处理和拦截器方便 | — | 1h |

---

## 五、UI Navigator 自动化

| 技术 / Setup | 实现的功能 | 为什么选择 | Dev A 耗时 | Dev B 耗时 |
|---|---|---|---|---|
| **Playwright (Python async)** | ① 控制 Chromium 浏览器，在买菜/外卖网站上执行搜索、点击、加购 ② 截取当前页面截图，发给 Gemini 分析 | 比赛要求 UI Navigator 必须用"截图→Gemini识别→执行动作"的闭环；Playwright 比 Puppeteer 对 Python 支持更好；异步 API 与 FastAPI 天然配合 | — | 10h (安装+基础配置) + 20h (UI 导航闭环攻关) |
| **playwright install chromium** | 下载 Chromium 浏览器二进制 | Playwright 运行必须，Cloud Run 容器中也需要单独安装 | — | 1h (含 Cloud Run 容器配置) |

---

## 六、容器化与部署

| 技术 / Setup | 实现的功能 | 为什么选择 | Dev A 耗时 | Dev B 耗时 |
|---|---|---|---|---|
| **Docker + Dockerfile** | 将 FastAPI + Playwright + Chromium 打包成可部署镜像 | Cloud Run 部署必须容器化；Playwright 需要 Chromium，Dockerfile 统一管理依赖 | 3h | — |
| **`cloudbuild.yaml`** | 自动化构建镜像并推送到 Cloud Run（IaC 自动化部署） | 满足比赛 +0.2 分的"自动化部署"加分项 | 1h | — |

---

## 七、开发工具与工作流

| 技术 / Setup | 实现的功能 | 为什么选择 | Dev A 耗时 | Dev B 耗时 |
|---|---|---|---|---|
| **GitHub (public repo)** | 代码版本管理、比赛提交必须提供公开代码库链接 | 比赛强制要求；评审要看 commit 历史和 README | 0.5h | 0.5h |
| **`requirements.txt`** | 固定 Python 依赖版本，保证本地/Cloud Run 一致 | Dockerfile 依赖它；README spin-up instructions 也要用它 | 0.5h | — |
| **`README.md`** | Spin-up 指南、架构说明、环境变量配置——评审打分重要依据 | 比赛明确要求有 step-by-step 的本地运行/部署文档 | 5h | — |
| **Architecture Diagram (draw.io / Excalidraw)** | 可视化展示 Gemini 如何连接后端、Firestore、Calendar、Playwright | 比赛提交必须包含架构图，Demo & Presentation 评分项（30%）重点 | 3h | — |
| **演示视频 (OBS/QuickTime + CapCut)** | 4 分钟内展示：上传小票→解析→决策→Playwright 自动加购完整闭环 | 比赛强制要求，且是"The Live Factor"评分核心，必须展示真实软件运行 | — | 10h |

---

## 八、时间汇总

| 模块 | Dev A 合计 | Dev B 合计 |
|---|---|---|
| GCP 基础设施 | ~10h | — |
| AI/Agent (SDK + Prompt) | ~21h | ~21h |
| 后端框架 | ~8h | — |
| 前端框架 | — | ~9h |
| Playwright UI 自动化 | — | ~31h |
| 容器化与部署 | ~4h | — |
| 文档、架构图、视频 | ~9h | ~11h |
| **合计** | **~52h** | **~72h** |

> 注：总计约 124 小时，与规划书 120–160 小时范围一致。B 的负担略重（UI 导航是最难攻关点），建议 Day 3–5 A 协助 B 调试 Playwright + Gemini 闭环。
