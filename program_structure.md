```
backend/
├── main.py                  # FastAPI 应用入口，注册路由、CORS、启动事件
├── routers/
│   ├── ocr.py               # /parse-receipt、/recommend 端点
│   ├── inventory.py         # /inventory CRUD 端点
│   └── navigator.py         # /navigate-search 端点
├── models/
│   └── schemas.py           # 所有 Pydantic 数据模型定义
├── services/
│   ├── gemini_service.py    # 封装 Google GenAI SDK 调用逻辑
│   ├── firestore_service.py # 封装 Firestore 读写操作
│   └── playwright_service.py# 封装 Playwright 截图与操作逻辑
├── .env                     # 本地密钥（不提交 Git）
└── requirements.txt
```

---

Port	运行什么	    谁访问它
8080	FastAPI 后端	前端、curl、Postman
3000	Next.js 前端	你的浏览器


你的浏览器
    │  打开 localhost:3000
    ▼
Next.js 前端 (port 3000)
    │  点击按钮后，Axios 发请求到 localhost:8080
    ▼
FastAPI 后端 (port 8080)
    │  调用 Gemini SDK
    ▼
Vertex AI / Gemini (GCP 云端)
    │  返回文字
    ▼
FastAPI → Next.js → 浏览器显示结果