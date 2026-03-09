# TrackBite — 阶梯式 Iterative Development 计划

> **今日日期**：2026-03-07（周六）
> **提交截止**：2026-03-16（周一）17:00 PT
> **实际可用天数**：10 天
> **团队**：Developer A（后端/逻辑）+ Developer B（前端/自动化）

---

## 前置分析：评分权重驱动迭代顺序

| 评分维度 | 权重 | 对迭代顺序的影响 |
|---|---|---|
| Innovation & Multimodal UX | 40% | 尽早展示"图片输入 → AI → 自动操作"闭环 |
| Technical Implementation | 30% | GCP Native、错误处理、防幻觉 |
| Demo & Presentation | 30% | 每个阶段都要有可录视频的 Working Demo |

---

## 关键降级决策（与原规划书相比）

在正式进入迭代前，以下降级释放约 **20-25h** 关键时间：

| 原规划 | 降级方案 | 节省时间 | 原因 |
|---|---|---|---|
| 体检报告 PDF OCR 解析 | 手动健康档案表单（勾选过敏原/疾病） | ~10h | PDF 解析调试风险高，Demo 效果差不多 |
| Google Calendar OAuth 完整集成 | 备用：手动"今晚日程"选择器 | ~4h | OAuth 配置阻塞风险，手动选择器同样能展示业务逻辑 |
| 真实外卖网站自动化 | 本地 Mock 购物 HTML 页作为主 Demo 靶 | ~8h | 真实网站有 Bot 检测 / CAPTCHA，Demo 必翻车 |
| Playwright 跑在 Cloud Run | Playwright 本地运行，只部署 FastAPI 到 Cloud Run | ~6h | Cloud Run + Chromium 容器配置复杂，GCP 证明只需 FastAPI 在线 |

---

## 迭代计划

---

### Iteration 0：地基与脚手架
**时间：Day 1（Mar 7）上午 ｜ 预计耗时：~4h ｜ 双人并行**

**交付内容**：
- GCP 项目创建 + Vertex AI API 启用
- GitHub 公开仓库建立（含 `.gitignore`、`requirements.txt`、`README.md` 骨架）
- FastAPI 后端：`/health` + `/gemini-test` 端点（向 Gemini 发一句话，返回响应）
- Next.js 前端：一个页面，显示 "Gemini Connected ✓" 并回显 Gemini 返回文字
- `.env` 环境变量结构确立

**本阶段可向评委展示**：
- GCP Console 截图（Vertex AI 已启用）—— 部署证明材料起点
- GitHub repo 有内容、有 commit 历史
- 浏览器打开前端，Gemini 正确响应

**为何此阶段就可展示**：满足评审 Stage 1 "baseline viability" 的技术栈核实。

---

### Iteration 1：多模态 OCR → 文字建议 + 手动购买链接
**时间：Day 1 下午 ～ Day 2（Mar 7-8）｜ 预计耗时：~9h**

**Dev A（后端）**：
- 编写收据 OCR Prompt → Gemini 返回结构化 JSON（食材名、数量、购买日期）
- `/parse-receipt` API 端点（接收图片，返回食材 JSON）
- `/recommend` API 端点（接收食材列表，返回膳食建议文字）

**Dev B（前端）**：
- 图片上传 UI（拖拽 / 点击）
- 解析结果展示：食材卡片列表
- 膳食建议卡片
- **"去购买"按钮**：硬编码跳转到购物网站搜索页（URL + 搜索词拼接），用户手动点击

**本阶段可向评委展示**：
> "上传一张超市小票 → AI 自动识别食材 → 推荐今晚吃什么 → 点击按钮跳转购物页"

评委可见：多模态输入（图片）、结构化 AI 输出、可操作建议。  
**此阶段"购买"由用户手动点链接完成** —— 这是有意为之的起点，后续迭代逐步接管。

---

### Iteration 2：健康档案 + 库存管理 → 更智能的决策
**时间：Day 3（Mar 9）｜ 预计耗时：~8h**

**Dev A（后端）**：
- Firestore 集成：存储食材库存（从 OCR 结果写入）+ 健康档案
- `/inventory` CRUD API
- 决策引擎升级：综合健康限制 + 当前库存 → 给出个性化推荐

**Dev B（前端）**：
- 健康档案页面：勾选框（过敏原：海鲜 / 坚果 / 乳糖；疾病：高血压 / 糖尿病；偏好：低碳 / 高蛋白）
- 库存看板：展示冰箱里有什么 + 距购买日期天数（用 OCR 日期推算）
- 上传小票后自动更新库存看板

**本阶段可向评委展示**：
> "系统知道我有高血压 + 冰箱里有豆腐和西红柿 → 推荐低钠番茄豆腐汤，而非高钠外卖"

评委可见：多维度 AI 推理（健康 + 库存）、Firestore 数据持久化、个性化建议。

---

### Iteration 3：日程感知 → 决定"做饭 / 点外卖 / 跳过"
**时间：Day 4（Mar 10）｜ 预计耗时：~7h**

**Dev A（后端）**：
- Google Calendar API 集成（OAuth + 读取今日事件）
- 决策逻辑：
  - 有晚间事件（加班 / 健身 / 聚餐）→ 推荐外卖，给出订购链接
  - 无事件 → 推荐做饭，给出买菜链接（此时仍为手动点击）
  - 已有聚餐 → "今晚已有外食计划，无需推荐"

**Dev B（前端）**：
- 首页顶部：日程卡片（今日事件摘要）
- 推荐卡片新增"频道"标签：🍳 做饭 / 🛵 点外卖 / ⏭️ 跳过

**备用降级**：若 Calendar OAuth 当天卡住，改为前端下拉选择器"今晚计划：加班 / 在家 / 健身 / 聚餐"，效果等同，节省 ~3h。

**本阶段可向评委展示**：
> "今天日历显示有加班到 10 点 → AI 决定点外卖 → 给出外卖推荐"

评委可见：三维度完整推理（Health + Inventory + Schedule）—— 系统"大脑"完整成型。

---

### Iteration 4：UI Navigator — Gemini 开始看屏幕（单步自动操作）
**时间：Day 4 下午 ～ Day 5（Mar 10-11）｜ 预计耗时：~11h**

**这是最关键的技术迭代，也是评分核心所在。**

**核心机制**（替换"手动点链接"）：
1. 后端收到"需要购买 X 食材"指令
2. Playwright 无头浏览器打开本地 Mock 购物页
3. 截图 → 发给 Gemini + Prompt：`"这是购物网站截图，搜索框在哪？返回元素描述或坐标"`
4. Gemini 返回位置描述
5. Playwright 在该位置输入搜索词
6. 二次截图 → Gemini 确认操作结果
7. 前端展示 Before / After 截图对比

**Dev A（后端）**：
- 设计 Gemini UI 识别 Prompt（核心，需反复测试）
- `/navigate-search` API 端点
- 截图存入 GCS，返回图片 URL

**Dev B（前端 + Playwright）**：
- Playwright 基础配置 + 截图功能
- 建立本地 Mock 购物 HTML 页（带搜索框 + 商品列表的简单页面）
- 前端展示：截图 Before/After + "Agent 正在思考..." 加载动画

**本阶段可向评委展示**：
> "Agent 打开购物网站截图 → 发给 Gemini → Gemini 识别搜索框位置 → 自动输入'西红柿' → 再次截图确认"

这正是评审标准中的 **"visual precision (understanding screen context) rather than blind clicking"**。

**⚠️ 关键原则**：本阶段先用 Mock 页确保 Demo 不崩，Walmart.com 等真实网站作为可选"惊喜彩蛋"。

---

### Iteration 5：全自动 UI Navigator 闭环（多步操作）
**时间：Day 6-7（Mar 12-13）｜ 预计耗时：~15h**

在 Iteration 4 基础上扩展为完整多步循环：

```
截图 1 → Gemini 识别搜索框 → 输入食材名
截图 2 → Gemini 识别第一个搜索结果 → 点击
截图 3 → Gemini 识别"加入购物车"按钮 → 点击
截图 4 → Gemini 确认已加入 → 返回成功状态
```

**Dev A（后端）**：
- 多步导航状态机（Step 1-4 循环结构）
- 每步独立的 Gemini Prompt 设计
- 错误处理：Gemini 置信度低 → 暂停并向用户请求确认

**Dev B（前端 + Playwright）**：
- 前端实时显示：步骤进度条 + 每步截图
- "代理正在操作..." 的动态状态流（Demo 视觉亮点）
- 完整流程：首页上传小票 → 最终"商品已加入购物车 ✓"成功状态

**本阶段可向评委展示**：
> 完整端到端 Demo：上传超市小票 → AI 分析健康 + 库存 + 日程 → 决定购买西红柿和豆腐 → 自动打开购物网站，Gemini 看着屏幕一步步操作，商品加入购物车

**这是 Demo 视频的主体片段，也是评分最高的 Wow Moment。**

---

### Iteration 6：打磨 + 部署 + 演示材料
**时间：Day 8-9（Mar 14-15）｜ 预计耗时：~14h**

**Dev A（后端 + 文档）**：
- Dockerfile：打包 FastAPI + 依赖项（Playwright 本地运行，不进容器）
- Cloud Run 部署 + 验证（后端 API 公网可访问）
- `cloudbuild.yaml` 自动化部署脚本（**+0.2 分加分项**）
- `README.md` 完整 spin-up 指南 + 架构说明 + 环境变量配置
- 架构图（draw.io / Excalidraw）

**Dev B（视频 + Devpost）**：
- 录制 Demo 视频（目标 3.5 分钟，留 30 秒 buffer）

  | 时间段 | 内容 |
  |---|---|
  | 0:00 - 0:30 | 问题陈述："每天纠结吃什么、食材过期、来不及买菜" |
  | 0:30 - 2:30 | 完整 Demo 流程（Iteration 5 全流程） |
  | 2:30 - 3:00 | 架构图讲解 + Gemini 如何驱动每步 |
  | 3:00 - 3:30 | GCP 部署证明（Cloud Run 控制台录屏） |

- 英文字幕
- Devpost 文字描述 + 架构图上传

**可选加分（Mar 15 如有余力）**：
- dev.to / Medium 发一篇 "How we built TrackBite with Gemini 3.0" → **+0.6 分**

---

### Day 10（Mar 16）：最终提交 Checklist

- [ ] GitHub 仓库公开，有清晰的 commit 历史
- [ ] `README.md` 有完整 spin-up 指南
- [ ] 架构图已上传至 Devpost
- [ ] 4 分钟内 Demo 视频（YouTube / Vimeo 公开链接）
- [ ] Cloud Run 部署证明截图 / 录屏
- [ ] Devpost 所有字段填写完整
- [ ] （可选）博客文章链接 (+0.6)
- [ ] （可选）`cloudbuild.yaml` 自动化部署 (+0.2)

---

## 总览表格

| 迭代 | 日期 | 总耗时 | 核心交付物 | 评委可见内容 |
|---|---|---|---|---|
| **0 地基** | Day 1 上午 (Mar 7) | ~4h | GCP + GitHub + Hello Gemini | GCP 部署证明、代码库建立 |
| **1 OCR + 手动链接** | Day 1-2 (Mar 7-8) | ~9h | 小票 → 食材 → 建议 → 手动跳转购买 | 多模态输入、结构化输出 |
| **2 健康 + 库存** | Day 3 (Mar 9) | ~8h | 健康档案 + Firestore 库存看板 | 多维推理、数据持久化 |
| **3 日程感知** | Day 4 (Mar 10) | ~7h | 日历 → 做饭 or 外卖决策 | 三维度完整"大脑"决策 |
| **4 Gemini 看屏幕** | Day 4-5 (Mar 10-11) | ~11h | 截图 → Gemini 识别 → 单步自动输入 | UI Navigator 核心能力首亮相 |
| **5 全自动导航** | Day 6-7 (Mar 12-13) | ~15h | 多步截图-识别-操作闭环 | 完整端到端 Demo，核心 Wow Moment |
| **6 打磨 + 交付** | Day 8-9 (Mar 14-15) | ~14h | 视频、Cloud Run、README、架构图 | 提交完整材料 |
| **最终提交** | Day 10 (Mar 16) | ~2h | Devpost 最终提交 | — |

**合计约 70h，两人各约 35h。**  
比原规划书 120-160h 精简约 55%，但评委能看到的全部核心价值点均保留。

---

## 关键风险与对策

| 风险 | 触发条件 | 对策 |
|---|---|---|
| Calendar OAuth 配置超时 | Day 4 结束仍未打通 | 切换为手动日程选择器，继续推进 Iteration 4 |
| 真实网站 Bot 检测 / CAPTCHA | Playwright 被封 | Mock 页作为主 Demo，真实网站作为可选"彩蛋" |
| Gemini 坐标识别不稳定 | Iteration 4-5 准确率低 | 降级为 Gemini 返回关键词 → Playwright 用 `page.get_by_text()` 定位，仍展示 Gemini 在"读屏幕" |
| Cloud Run + Playwright 配置失败 | Day 8 容器化失败 | Playwright 本地运行，只部署 FastAPI 到 Cloud Run，满足 GCP 证明要求 |
| 时间不足，Iteration 5 未完成 | Day 7 结束仍有 bug | Demo 停留在 Iteration 4（单步导航），这已满足 UI Navigator 评分核心要求 |
